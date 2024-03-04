from src.api.public.main import *

def history(usr):
    data = action.objects.filter(user_id=usr.id, active=True, removed=False).order_by('-id')
    data = data.filter(
        Q(type='register')|Q(type='login')|Q(type='edit_account')|
        Q(type='withdraw')|Q(type='confirm_withdraw')|Q(type='deposit')
    )
    data = [ch for ch in data.values()]
    return data

@auth_admin
def index(request, usr):
    data = user.objects.filter(id=usr.id, active=True, removed=False, role=1).values().first()
    if not data: return response()
    del data['password']
    return response(status=True, user=data, activity=history(usr))

@auth_admin
def save(request, usr):
    config = user.objects.filter(id=usr.id, active=True, removed=False, role=1).first()
    if not config: return response()
    email = request.POST.get('email')
    if user.objects.filter(email=email, removed=False).exclude(id=usr.id).exists():
        return response(status='exists')
    config.name = request.POST.get('name')
    config.email = request.POST.get('email')
    config.phone = request.POST.get('phone')
    config.age = double(request.POST.get('age'))
    config.country = request.POST.get('country')
    config.city = request.POST.get('city')
    config.street = request.POST.get('street')
    config.language = request.POST.get('language')
    config.currency = request.POST.get('currency')
    config.update_date = get_date()
    image = request.FILES.get('file')
    if image:
        image = upload_file(dir='user', file=image, ext=request.POST.get('ext'))
        remove_file(f'user/{config.image}')
        config.image = image
    config.save()
    data = user.objects.filter(id=usr.id).values().first()
    del data['password']
    return response(status=True, user=data, activity=history(usr))

@auth_admin
def password(request, usr):
    config = user.objects.filter(id=usr.id, active=True, removed=False, role=1).first()
    if not config: return response()
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    if config.password != old_password:
        return response(status='not_match')
    config.password = new_password
    config.save()
    return response(status=True)

@auth_admin
def delete(request, usr):
    ids = parse(request.POST.get('ids'))
    for id in ids:
        config = action.objects.filter(id=id).first()
        if not config: continue
        config.active = False
        config.save()
    return response(status=True)
