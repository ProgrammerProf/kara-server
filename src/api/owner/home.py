from src.api.public.main import *

def recently_bookings(usr):
    items = booking.objects.filter(owner_id=usr.id, removed=False).order_by('-id')[:10]
    data = []
    for item in items.values():
        item['coupon_code'] = item['coupon']
        config_product = product.objects.filter(id=item['product_id'], owner_id=usr.id).first()
        if config_product:
            image = file.objects.filter(product_id=config_product.id, type='image').first()
            image = image.id if image else 0
            item['product'] = {'id': config_product.id, 'name': config_product.name, 'image': image}
            item['product_id'] = config_product.id
            item['product_name'] = config_product.name
        config_user = user.objects.filter(id=item['user_id']).first()
        if config_user:
            item['user'] = {'id': config_user.id, 'name': config_user.name}
            item['user_id'] = config_user.id
            item['user_name'] = config_user.name
        data.append(item)
    return data

def series(items, limit='daily', views=False):
    duration, rng = 0, 0
    if limit == 'daily': duration, rng = 86400, 7
    if limit == 'weekly': duration, rng = 604800, 7
    if limit == 'monthly': duration, rng = 2592000, 12
    if limit == 'yearly': duration, rng = 31536000, 7
    data = [0 for ch in range(rng)]
    for item in items:
        dt = diff_date(item.create_date)
        for i in range(1, rng+1):
            if duration * i >= dt and dt > duration * (i-1):
                if views: data[i-1] += item.views
                else: data[i-1] += 1
                break
    return list(reversed(data))

def calculate(items, views=False):
    total = items.count()
    if views: total = sum([ch.views for ch in items])
    data = {
        'total': total,
        'series_daily': series(items, 'daily', views),
        'series_weekly': series(items, 'weekly', views),
        'series_monthly': series(items, 'monthly', views),
        'series_yearly': series(items, 'yearly', views),
    }
    return data

@auth_owner
def statistics(request, usr):
    data = {}
    if usr.statistics:
        data = {
            'visitors': calculate(product.objects.filter(owner_id=usr.id, removed=False), views=True),
            'products': calculate(product.objects.filter(owner_id=usr.id, removed=False)),
            'coupons': calculate(coupon.objects.filter(owner_id=usr.id)),
            'bookings': calculate(booking.objects.filter(owner_id=usr.id, removed=False)),
            'confirmed': calculate(booking.objects.filter(owner_id=usr.id, removed=False, status=4)),
            'cancelled': calculate(booking.objects.filter(owner_id=usr.id, removed=False, status=3)),
            'settings': {'balance': usr.balance, 'profit': usr.profit, 'income': usr.income, 'expenses': usr.expenses}
        }
    if usr.see_bookings: data['recently_bookings'] = recently_bookings(usr)
    if usr.see_products:
        products = product.objects.filter(owner_id=usr.id, removed=False).order_by('-id').values()[:10]
        data['recently_products'] = [ch for ch in products]
    return response(status=True, **data)
