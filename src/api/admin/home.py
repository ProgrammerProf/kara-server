from src.api.public.main import *

def recently_bookings():
    items = booking.objects.filter(removed=False).order_by('-id')[:10]
    data = []
    for item in items.values():
        item['coupon_code'] = item['coupon']
        config_product = product.objects.filter(id=item['product_id']).first()
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

def series(items, limit='daily'):
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
                data[i-1] += 1
                break
    return list(reversed(data))

def calculate(items):
    data = {
        'total': items.count(),
        'series_daily': series(items, 'daily'),
        'series_weekly': series(items, 'weekly'),
        'series_monthly': series(items, 'monthly'),
        'series_yearly': series(items, 'yearly'),
    }
    return data

@auth_admin
def statistics(request, usr):
    data = {}
    if usr.statistics:
        data = {
            'visitors': calculate(user.objects.filter(removed=False, role=3)),
            'categories': calculate(category.objects.all()),
            'properties': calculate(product.objects.filter(removed=False)),
            'coupons': calculate(coupon.objects.all()),
            'bookings': calculate(booking.objects.filter(removed=False)),
            'confirmed': calculate(booking.objects.filter(removed=False, status=4)),
            'cancelled': calculate(booking.objects.filter(removed=False, status=3)),
            'settings': setting.objects.filter(active=True).values().first(),
            'users': {
                'Admins': user.objects.filter(removed=False, role=1).count(),
                'Owners': user.objects.filter(removed=False, role=2).count(),
                'Guests': user.objects.filter(removed=False, role=3).count(),
            },
        }
    if usr.see_bookings:
        data['recently_bookings'] = recently_bookings()
    if usr.see_products:
        data['recently_products'] = [ch for ch in product.objects.filter(removed=False).order_by('-id').values()[:10]]
    if usr.see_owners and usr.see_guests:
        data['recently_users'] = [ch for ch in user.objects.filter(Q(role=2, removed=False)|Q(role=3, removed=False)).order_by('-id').values()[:10]]
    elif usr.see_owners and not usr.see_guests:
        data['recently_users'] = [ch for ch in user.objects.filter(role=2, removed=False).order_by('-id').values()[:10]]
    elif not usr.see_owners and usr.see_guests:
        data['recently_users'] = [ch for ch in user.objects.filter(role=3, removed=False).order_by('-id').values()[:10]]
    return response(status=True, **data)
