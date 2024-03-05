from src.api.public.main import *

@auth_admin
def index(request, usr):
    id = integer(request.POST.get('id'))
    role = integer(request.POST.get('role'))
    if role == 1 and not usr.supervisor: return response()
    if role == 2 and not usr.see_owners: return response()
    if role == 3 and not usr.see_guests: return response()
    if id:
        if role == 1 and usr.supervisor and not usr.super:
            items = user.objects.filter(id=id, role=role, super=False, admin_id=usr.id, removed=False)
        else:
            items = user.objects.filter(id=id, role=role, super=False, removed=False)
        if usr == id: return response()
    else:
        if role == 1 and usr.supervisor and not usr.super:
            items = user.objects.filter(role=role, super=False, admin_id=usr.id, removed=False).exclude(id=usr.id).order_by('-id')
        else:
            items = user.objects.filter(role=role, super=False, removed=False).exclude(id=usr.id).order_by('-id')
    data = []
    for item in items.values():
        item['products'] = product.objects.filter(owner_id=item['id'], removed=False).count()
        data.append(item)
    if id: data = data[0] if data else {}
    return response(data=data)

@auth_admin
def add(request, usr):
    role = integer(request.POST.get('role'))
    if role == 1 and not usr.supervisor: return response()
    if role == 2 and (not usr.see_owners or not usr.add_owners): return response()
    if role == 3 and (not usr.see_guests or not usr.add_guests): return response()
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')
    country = request.POST.get('country')
    city = request.POST.get('city')
    street = request.POST.get('street')
    age = integer(request.POST.get('age'))
    balance = double(request.POST.get('balance'))
    salary = double(request.POST.get('salary'))
    notes = request.POST.get('notes')
    chat = bool(request.POST.get('chat'))
    mail = bool(request.POST.get('mail'))
    see_categories = bool(request.POST.get('see_categories'))
    add_categories = bool(request.POST.get('add_categories'))
    delete_categories = bool(request.POST.get('delete_categories'))
    see_products = bool(request.POST.get('see_products'))
    add_products = bool(request.POST.get('add_products'))
    delete_products = bool(request.POST.get('delete_products'))
    see_bookings = bool(request.POST.get('see_bookings'))
    add_bookings = bool(request.POST.get('add_bookings'))
    delete_bookings = bool(request.POST.get('delete_bookings'))
    see_coupons = bool(request.POST.get('see_coupons'))
    add_coupons = bool(request.POST.get('add_coupons'))
    delete_coupons = bool(request.POST.get('delete_coupons'))
    see_owners = bool(request.POST.get('see_owners'))
    add_owners = bool(request.POST.get('add_owners'))
    delete_owners = bool(request.POST.get('delete_owners'))
    see_guests = bool(request.POST.get('see_guests'))
    add_guests = bool(request.POST.get('add_guests'))
    delete_guests = bool(request.POST.get('delete_guests'))
    control_owners_balance = bool(request.POST.get('control_owners_balance'))
    control_guests_balance = bool(request.POST.get('control_guests_balance'))
    allow_products = bool(request.POST.get('allow_products'))
    allow_coupons = bool(request.POST.get('allow_coupons'))
    allow_bookings = bool(request.POST.get('allow_bookings'))
    notifications = bool(request.POST.get('notifications'))
    statistics = bool(request.POST.get('statistics'))
    supervisor = bool(request.POST.get('supervisor'))
    active = bool(request.POST.get('active'))
    if user.objects.filter(email=email, removed=False).first():
        return response(status='exists')
    image = upload_file(dir='user', file=request.FILES.get('file'), ext=request.POST.get('ext'))
    user(
        name=name, phone=phone, email=email, password=password, country=country,
        city=city, street=street, age=age, notes=notes, chat=chat, mail=mail, admin_id=usr.id,
        create_date=get_date(), update_date=get_date(), login_date=get_date(), image=image,
        ip=client(request, 'ip'), host=client(request, 'host'), role=role, salary=salary, balance=balance,
        see_categories=see_categories, add_categories=add_categories, delete_categories=delete_categories,
        see_products=see_products, add_products=add_products, delete_products=delete_products,
        see_bookings=see_bookings, add_bookings=add_bookings, delete_bookings=delete_bookings,
        see_coupons=see_coupons, add_coupons=add_coupons, delete_coupons=delete_coupons,
        see_owners=see_owners, add_owners=add_owners, delete_owners=delete_owners,
        see_guests=see_guests, add_guests=add_guests, delete_guests=delete_guests,
        allow_products=allow_products, allow_coupons=allow_coupons, allow_bookings=allow_bookings,
        notifications=notifications, statistics=statistics, active=active, supervisor=supervisor,
        control_owners_balance=control_owners_balance, control_guests_balance=control_guests_balance,
    ).save()
    id = user.objects.latest('id').id
    record_action(
        request, user_id=usr.id,
        type=f'add_{"admin" if role == 1 else "owner" if role == 2 else "guest"}',
        action_id=id
    )
    return response(status=True)

@auth_admin
def edit(request, usr):
    id = integer(request.POST.get('id'))
    role = integer(request.POST.get('role'))
    if role == 1 and not usr.supervisor: return response()
    if role == 2 and not usr.see_owners: return response()
    if role == 3 and not usr.see_guests: return response()
    config = user.objects.filter(id=id, role=role, super=False, removed=False).first()
    if not config or usr == config.id: return response()
    if role == 1 and usr.supervisor and not usr.super:
        if config.admin_id != usr.id: return response()
    email = request.POST.get('email')
    if user.objects.filter(email=email, removed=False).exclude(id=id).first():
        return response(status='exists')
    config.name = request.POST.get('name')
    config.phone = request.POST.get('phone')
    config.email = request.POST.get('email')
    config.password = request.POST.get('password')
    config.country = request.POST.get('country')
    config.city = request.POST.get('city')
    config.street = request.POST.get('street')
    config.age = integer(request.POST.get('age'))
    config.balance = double(request.POST.get('balance'))
    config.salary = double(request.POST.get('salary'))
    config.notes = request.POST.get('notes')
    config.chat = bool(request.POST.get('chat'))
    config.mail = bool(request.POST.get('mail'))
    config.see_categories = bool(request.POST.get('see_categories'))
    config.add_categories = bool(request.POST.get('add_categories'))
    config.delete_categories = bool(request.POST.get('delete_categories'))
    config.see_products = bool(request.POST.get('see_products'))
    config.add_products = bool(request.POST.get('add_products'))
    config.delete_products = bool(request.POST.get('delete_products'))
    config.see_bookings = bool(request.POST.get('see_bookings'))
    config.add_bookings = bool(request.POST.get('add_bookings'))
    config.delete_bookings = bool(request.POST.get('delete_bookings'))
    config.see_coupons = bool(request.POST.get('see_coupons'))
    config.add_coupons = bool(request.POST.get('add_coupons'))
    config.delete_coupons = bool(request.POST.get('delete_coupons'))
    config.see_owners = bool(request.POST.get('see_owners'))
    config.add_owners = bool(request.POST.get('add_owners'))
    config.delete_owners = bool(request.POST.get('delete_owners'))
    config.see_guests = bool(request.POST.get('see_guests'))
    config.add_guests = bool(request.POST.get('add_guests'))
    config.delete_guests = bool(request.POST.get('delete_guests'))
    config.control_owners_balance = bool(request.POST.get('control_owners_balance'))
    config.control_guests_balance = bool(request.POST.get('control_guests_balance'))
    config.allow_products = bool(request.POST.get('allow_products'))
    config.allow_coupons = bool(request.POST.get('allow_coupons'))
    config.allow_bookings = bool(request.POST.get('allow_bookings'))
    config.notifications = bool(request.POST.get('notifications'))
    config.statistics = bool(request.POST.get('statistics'))
    config.supervisor = bool(request.POST.get('supervisor'))
    config.active = bool(request.POST.get('active'))
    config.update_date = get_date()
    f = request.FILES.get('file')
    if f:
        image = upload_file(dir='user', file=f, ext=request.POST.get('ext'))
        remove_file(f'user/{config.image}')
        config.image = image
    config.save()
    record_action(
        request, user_id=usr.id,
        type=f'edit_{"admin" if role == 1 else "owner" if role == 2 else "guest"}',
        action_id=config.id
    )
    return response(status=True)

@auth_admin
def delete(request, usr):
    ids = parse(request.POST.get('ids'))
    role = integer(request.POST.get('role'))
    if role == 1 and not usr.supervisor: return response()
    if role == 2 and (not usr.see_owners or not usr.delete_owners): return response()
    if role == 3 and (not usr.see_guests or not usr.delete_guests): return response()
    for id in ids:
        config = user.objects.filter(id=id, role=role, removed=False, super=False).first()
        if not config: continue
        if role == 1 and usr.supervisor and not usr.super:
            if config.admin_id != usr.id: continue
        config.removed = True
        config.removed_date = get_date()
        config.save()
        for item in product.objects.filter(owner_id=id):
            item.owner_id = 0
            item.save()
        record_action(
            request, user_id=usr.id,
            type=f'delete_{"admin" if role == 1 else "owner" if role == 2 else "guest"}',
            action_id=id
        )
    return response(status=True)
