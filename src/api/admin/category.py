from src.api.public.main import *

@auth_admin
def index(request, usr):
    if not usr.see_categories: return response()
    id = integer(request.POST.get('id'))
    if id: items = category.objects.filter(id=id)
    else: items = category.objects.all().order_by('-id')
    data = []
    for item in items.values():
        item['products'] = product.objects.filter(category_id=item['id'], removed=False).count()
        data.append(item)
    if id: data = data[0] if data else {}
    return response(data=data)

@auth_admin
def add(request, usr):
    if not usr.see_categories or not usr.add_categories: return response()
    name = request.POST.get('name')
    description = request.POST.get('description')
    location = request.POST.get('location')
    company = request.POST.get('company')
    phone = request.POST.get('phone')
    allow_products = bool(request.POST.get('allow_products'))
    active = bool(request.POST.get('active'))
    if category.objects.filter(name=name).first():
        return response(status='exists')
    image = upload_file(dir='category', file=request.FILES.get('file'), ext=request.POST.get('ext'))
    category(
        name=name, description=description, company=company, phone=phone,
        location=location, allow_products=allow_products, active=active, create_date=get_date(),
        update_date=get_date(), image=image
    ).save()
    id = category.objects.latest('id').id
    record_action(request, user_id=usr.id, type='add_category', action_id=id)
    return response(status=True)

@auth_admin
def edit(request, usr):
    if not usr.see_categories: return response()
    id = integer(request.POST.get('id'))
    config = category.objects.filter(id=id).first()
    if not config: return response()
    name = request.POST.get('name')
    if category.objects.filter(name=name).exclude(id=id).first():
        return response(status='exists')
    config.name = request.POST.get('name')
    config.description = request.POST.get('description')
    config.location = request.POST.get('location')
    config.company = request.POST.get('company')
    config.phone = request.POST.get('phone')
    config.allow_products = bool(request.POST.get('allow_products'))
    config.active = bool(request.POST.get('active'))
    config.update_date = get_date()
    f = request.FILES.get('file')
    if f:
        image = upload_file(dir='category', file=f, ext=request.POST.get('ext'))
        remove_file(f'category/{config.image}')
        config.image = image
    config.save()
    record_action(request, user_id=usr.id, type='edit_category', action_id=config.id)
    return response(status=True)

@auth_admin
def delete(request, usr):
    if not usr.see_categories or not usr.delete_categories: return response()
    ids = parse(request.POST.get('ids'))
    for id in ids:
        config = category.objects.filter(id=id).first()
        if not config: continue
        remove_file(f'category/{config.image}')
        config.delete()
        items = product.objects.filter(category_id=id)
        for item in items:
            item.category_id = 0
            item.save()
        record_action(request, user_id=usr.id, type='delete_category', action_id=id)
    return response(status=True)
