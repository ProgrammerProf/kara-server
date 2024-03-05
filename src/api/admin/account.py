from src.api.public.main import *

def history(usr):
    data = action.objects.filter(user_id=usr.id, active=True, removed=False).order_by('-id')
    data = data.filter(
        Q(type='register')|Q(type='login')|Q(type='edit_account')|Q(type='change_password')|
        Q(type='withdraw')|Q(type='confirm_withdraw')|Q(type='deposit')
    )
    data = [ch for ch in data.values()]
    return data

@auth_admin
def index(request, usr):
    data = user.objects.filter(id=usr.id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data, activity=history(usr))

@auth_admin
def save(request, usr):
    if user.objects.filter(email=request.POST.get('email')).exclude(id=usr.id).exists():
        return response(status='exists')
    usr.name = request.POST.get('name')
    usr.email = request.POST.get('email')
    usr.phone = request.POST.get('phone')
    usr.age = double(request.POST.get('age'))
    usr.country = request.POST.get('country')
    usr.city = request.POST.get('city')
    usr.street = request.POST.get('street')
    usr.language = request.POST.get('language')
    usr.currency = request.POST.get('currency')
    usr.update_date = get_date()
    image = request.FILES.get('file')
    if image:
        image = upload_file(dir='user', file=image, ext=request.POST.get('ext'))
        remove_file(f'user/{usr.image}')
        usr.image = image
    usr.save()
    record_action(request, user_id=usr.id, type='edit_account')
    data = user.objects.filter(id=usr.id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data, activity=history(usr))

@auth_admin
def password(request, usr):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    if old_password != usr.password: return response(status='not_match')
    usr.password = new_password
    usr.update_date = get_date()
    usr.save()
    record_action(request, user_id=usr.id, type='change_password')
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
