from src.api.public.main import *

def product_image(id=0):
    data = product.objects.filter(id=id, removed=False).first()
    if not data: return {}
    files = file.objects.filter(product_id=id)
    images_ = [['image', ch.id] for ch in files if ch.type == "image"]
    videos_ = [['video', ch.id] for ch in files if ch.type == "video"]
    images = videos_ + images_
    image = images_[0][1] if images else ''
    return image, images

def default_data():
    categories = category.objects.filter(active=True, allow_products=True).order_by('-id')
    owners = user.objects.filter(active=True, removed=False, role=2).order_by('-id')
    data = {
        'categories': [item for item in categories.values()],
        'owners': [item for item in owners.values()],
    }
    return data

@auth_admin
def default(request, usr):
    if not usr.see_products or not usr.add_products: return response()
    return response(**default_data())

@auth_admin
def index(request, usr):
    if not usr.see_products: return response()
    id = integer(request.POST.get('id'))
    if id: items = product.objects.filter(id=id, removed=False)
    else: items = product.objects.filter(removed=False).order_by('-id')
    data = []
    for item in items.values():
        item['image'], item['files'] = product_image(item['id'])
        item['details'] = {'name': item['name'], 'image_id': item['image']}
        section = category.objects.filter(id=item['category_id']).first()
        owner = user.objects.filter(id=item['owner_id']).first()
        if section: item['category'] = {'id': section.id, 'name': section.name}
        if owner: item['owner'] = {'id': owner.id, 'name': owner.name}
        data.append(item)
    if id:
        data = data[0] if data else {}
        data['categories'] = default_data()['categories']
        data['owners'] = default_data()['owners']
    return response(data=data)

@auth_admin
def add(request, usr):
    if not usr.see_products or not usr.add_products: return response()
    category_id = integer(request.POST.get('category'))
    owner_id = integer(request.POST.get('owner'))
    name = request.POST.get('name')
    country = request.POST.get('country')
    city = request.POST.get('city')
    street = request.POST.get('street')
    location = request.POST.get('location')
    phone = request.POST.get('phone')
    description = request.POST.get('description')
    overview = request.POST.get('overview')
    availability = request.POST.get('availability')
    policy = request.POST.get('policy')
    rules = request.POST.get('rules')
    safety = request.POST.get('safety')
    notes = request.POST.get('notes')
    new_price = double(request.POST.get('new_price'), 2)
    old_price = double(request.POST.get('old_price'), 2)
    rate = double(request.POST.get('rate'))
    adults = integer(request.POST.get('adults'))
    rooms = integer(request.POST.get('rooms'))
    beds = integer(request.POST.get('beds'))
    bedrooms = integer(request.POST.get('bedrooms'))
    bathrooms = integer(request.POST.get('bathrooms'))
    desert_view = bool(request.POST.get('desert_view'))
    sea_view = bool(request.POST.get('sea_view'))
    hair_dryer = bool(request.POST.get('hair_dryer'))
    cleaning_properties = bool(request.POST.get('cleaning_properties'))
    washing_machine = bool(request.POST.get('washing_machine'))
    iron = bool(request.POST.get('iron'))
    indoor_stove = bool(request.POST.get('indoor_stove'))
    wifi = bool(request.POST.get('wifi'))
    kitchen = bool(request.POST.get('kitchen'))
    refrigerator = bool(request.POST.get('refrigerator'))
    oven = bool(request.POST.get('oven'))
    television = bool(request.POST.get('television'))
    air_conditioner = bool(request.POST.get('air_conditioner'))
    dining_table = bool(request.POST.get('dining_table'))
    ceiling_fan = bool(request.POST.get('ceiling_fan'))
    desk_fan = bool(request.POST.get('desk_fan'))
    necessities = bool(request.POST.get('necessities'))
    allow_bookings = bool(request.POST.get('allow_bookings'))
    cancellation = bool(request.POST.get('cancellation'))
    pay_later = bool(request.POST.get('pay_later'))
    active = bool(request.POST.get('active'))
    product(
        name=name, country=country, city=city, street=street, phone=phone,
        location=location, active=active, create_date=get_date(),
        update_date=get_date(), category_id=category_id, owner_id=owner_id,
        allow_bookings=allow_bookings, description=description, overview=overview,
        availability=availability, policy=policy, rules=rules, safety=safety, notes=notes,
        new_price=new_price, old_price=old_price, rate=rate, adults=adults, rooms=rooms,
        beds=beds, bedrooms=bedrooms, bathrooms=bathrooms, desert_view=desert_view, iron=iron,
        sea_view=sea_view, hair_dryer=hair_dryer, cleaning_properties=cleaning_properties,
        washing_machine=washing_machine, indoor_stove=indoor_stove, wifi=wifi, kitchen=kitchen,
        refrigerator=refrigerator, oven=oven, television=television, air_conditioner=air_conditioner,
        dining_table=dining_table, ceiling_fan=ceiling_fan, desk_fan=desk_fan, necessities=necessities,
        cancellation=cancellation, pay_later=pay_later,
    ).save()
    id = product.objects.latest('id').id
    upload_files(request, id, 'product')
    record_action(request, user_id=usr.id, type='add_product', action_id=id)
    return response(status=True)

@auth_admin
def edit(request, usr):
    if not usr.see_products: return response()
    id = integer(request.POST.get('id'))
    config = product.objects.filter(id=id, removed=False).first()
    if not config: return response()
    config.category_id = integer(request.POST.get('category'))
    config.owner_id = integer(request.POST.get('owner'))
    config.name = request.POST.get('name')
    config.country = request.POST.get('country')
    config.city = request.POST.get('city')
    config.street = request.POST.get('street')
    config.location = request.POST.get('location')
    config.phone = request.POST.get('phone')
    config.description = request.POST.get('description')
    config.overview = request.POST.get('overview')
    config.availability = request.POST.get('availability')
    config.policy = request.POST.get('policy')
    config.rules = request.POST.get('rules')
    config.safety = request.POST.get('safety')
    config.notes = request.POST.get('notes')
    config.new_price = double(request.POST.get('new_price'), 2)
    config.old_price = double(request.POST.get('old_price'), 2)
    config.rate = double(request.POST.get('rate'))
    config.adults = integer(request.POST.get('adults'))
    config.rooms = integer(request.POST.get('rooms'))
    config.beds = integer(request.POST.get('beds'))
    config.bedrooms = integer(request.POST.get('bedrooms'))
    config.bathrooms = integer(request.POST.get('bathrooms'))
    config.desert_view = bool(request.POST.get('desert_view'))
    config.sea_view = bool(request.POST.get('sea_view'))
    config.hair_dryer = bool(request.POST.get('hair_dryer'))
    config.cleaning_properties = bool(request.POST.get('cleaning_properties'))
    config.washing_machine = bool(request.POST.get('washing_machine'))
    config.iron = bool(request.POST.get('iron'))
    config.indoor_stove = bool(request.POST.get('indoor_stove'))
    config.wifi = bool(request.POST.get('wifi'))
    config.kitchen = bool(request.POST.get('kitchen'))
    config.refrigerator = bool(request.POST.get('refrigerator'))
    config.oven = bool(request.POST.get('oven'))
    config.television = bool(request.POST.get('television'))
    config.air_conditioner = bool(request.POST.get('air_conditioner'))
    config.dining_table = bool(request.POST.get('dining_table'))
    config.ceiling_fan = bool(request.POST.get('ceiling_fan'))
    config.desk_fan = bool(request.POST.get('desk_fan'))
    config.necessities = bool(request.POST.get('necessities'))
    config.allow_bookings = bool(request.POST.get('allow_bookings'))
    config.cancellation = bool(request.POST.get('cancellation'))
    config.pay_later = bool(request.POST.get('pay_later'))
    config.active = bool(request.POST.get('active'))
    config.update_date = get_date()
    config.save()
    upload_files(request, id, 'product')
    record_action(request, user_id=usr.id, type='edit_product', action_id=config.id)
    return response(status=True)

@auth_admin
def delete(request, usr):
    if not usr.see_products or not usr.delete_products: return response()
    ids = parse(request.POST.get('ids'))
    for id in ids:
        config = product.objects.filter(id=id, removed=False).first()
        if not config: continue
        config.removed = True
        config.removed_date = get_date()
        config.save()
        items = file.objects.filter(product_id=id)
        for item in items:
            remove_file(f'product/{item.link}')
            item.delete()
        record_action(request, user_id=usr.id, type='delete_product', action_id=id)
    return response(status=True)
