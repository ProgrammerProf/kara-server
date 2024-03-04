from src.api.public.main import *

@auth_admin
def default(request, usr):
    if not usr.see_bookings or not usr.add_bookings: return response()
    products = product.objects.filter(active=True, removed=False, allow_bookings=True).order_by('-id')
    users = user.objects.filter(active=True, removed=False, role=3, allow_bookings=True).order_by('-id')
    coupons = coupon.objects.filter(active=True).order_by('-id')
    products_list = []
    for item in products.values():
        f = file.objects.filter(product_id=item['id'], type='image').first()
        if f: item['image'] = f.id
        products_list.append(item)
    data = {
        'products': products_list,
        'users': [item for item in users.values()],
        'coupons': [item for item in coupons.values()],
    }
    return response(**data)

@auth_admin
def index(request, usr):
    if not usr.see_bookings: return response()
    id = integer(request.POST.get('id'))
    if id: items = booking.objects.filter(id=id, removed=False)
    else: items = booking.objects.filter(removed=False).order_by('-id')
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
    if id: data = data[0] if data else {}
    return response(data=data)

@auth_admin
def add(request, usr):
    if not usr.see_bookings or not usr.add_bookings: return response()
    admin_id = integer(request.POST.get('user'))
    user_id = integer(request.POST.get('user_id'))
    product_id = integer(request.POST.get('product_id'))
    coupon_id = integer(request.POST.get('coupon_id'))
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    booking_date = request.POST.get('booking_date')
    notes = request.POST.get('notes')
    status = integer(request.POST.get('status'))
    paid = bool(request.POST.get('paid'))
    active = bool(request.POST.get('active'))
    config_user = user.objects.filter(id=user_id).first()
    config_product = product.objects.filter(id=product_id).first()
    config_coupon = coupon.objects.filter(id=coupon_id).first()
    if not config_user: return response(status=False)
    if not config_user.allow_bookings: return response(status=False)
    if not config_product: return response(status=False)
    if not config_product.allow_bookings: return response(status=False)
    config_owner = user.objects.filter(id=config_product.owner_id).first()
    if config_owner:
        if not config_owner.allow_bookings: return response(status=False)
    coupon_code = ''
    discount = 0
    price = config_product.new_price
    if config_coupon:
        discount = config_coupon.discount
        price -= (price * discount / 100)
        coupon_code = config_coupon.code
    booking(
        name=name, email=email, phone=phone, address=address, booking_date=booking_date,
        notes=notes, status=status, paid=paid, active=active, create_date=get_date(),
        update_date=get_date(), admin_id=admin_id, user_id=user_id, product_id=product_id,
        coupon=coupon_code, discount=discount, price=round(price, 2)
    ).save()
    return response(status=True)

@auth_admin
def edit(request, usr):
    if not usr.see_bookings: return response()
    id = integer(request.POST.get('id'))
    config = booking.objects.filter(id=id, removed=False).first()
    if not config: return response()
    config.name = request.POST.get('name')
    config.email = request.POST.get('email')
    config.phone = request.POST.get('phone')
    config.address = request.POST.get('address')
    config.booking_date = request.POST.get('booking_date')
    config.notes = request.POST.get('notes')
    config.status = integer(request.POST.get('status'))
    config.paid = bool(request.POST.get('paid'))
    config.active = bool(request.POST.get('active'))
    config.update_date = get_date()
    config.save()
    return response(status=True)

@auth_admin
def delete(request, usr):
    if not usr.see_bookings or not usr.delete_bookings: return response()
    ids = parse(request.POST.get('ids'))
    for id in ids:
        config = booking.objects.filter(id=id, removed=False).first()
        if not config: continue
        config.removed = True
        config.removed_date = get_date()
        config.save()
    return response(status=True)
