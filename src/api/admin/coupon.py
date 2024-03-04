from src.api.public.main import *

@auth_admin
def index(request, usr):
    if not usr.see_coupon: return response()
    id = integer(request.POST.get('id'))
    if id: items = coupon.objects.filter(id=id)
    else: items = coupon.objects.all().order_by('-id')
    data = [item for item in items.values()]
    if id: data = data[0] if data else {}
    return response(data=data)

@auth_admin
def add(request, usr):
    if not usr.see_coupon or not usr.add_coupon: return response()
    code = request.POST.get("code")
    discount = double(request.POST.get("discount"), 2)
    active = bool(request.POST.get("active"))
    if coupon.objects.filter(code=code).exists():
        return response(status='exists')
    coupon(
        code=code, discount=discount, active=active,
        create_date=get_date(), update_date=get_date()
    ).save()
    id = coupon.objects.latest('id').id
    return response(status=True, id=id)

@auth_admin
def edit(request, usr):
    if not usr.see_coupon: return response()
    id = integer(request.POST.get('id'))
    config = coupon.objects.filter(id=id).first()
    if not config: return response()
    code = request.POST.get('code')
    if coupon.objects.filter(code=code).exclude(id=id).first():
        return response(status='exists')
    config.code = request.POST.get('code')
    config.discount = double(request.POST.get('discount'), 2)
    config.active = bool(request.POST.get('active'))
    config.update_date = get_date()
    config.save()
    return response(status=True)

@auth_admin
def delete(request, usr):
    if not usr.see_coupon or not usr.delete_coupon: return response()
    ids = parse(request.POST.get('ids'))
    for id in ids:
        coupon.objects.filter(id=id).delete()
    return response(status=True)
