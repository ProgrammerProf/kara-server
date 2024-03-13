from src.api.public.main import *

@auth_admin
def index(request, usr):
    data = user.objects.filter(id=usr.id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data)

@auth_admin
def unlock(request, usr):
    password = request.POST.get('password')
    if password != usr.password: return response()
    data = user.objects.filter(id=usr.id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data)

@auth_api
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    config = user.objects.filter(role=1, email=email, active=True, removed=False).first()
    if not config: return response(status='exists')
    if password != config.password: return response(status='not_match')
    if not config.super:
        settings = setting.objects.filter(active=True).first()
        if not settings.admin_login: return response(status='logout')
    config.login_date = get_date()
    config.login_ip = client(request, 'ip')
    config.login_host = client(request, 'host')
    config.save()
    record_action(request, user_id=config.id, type='login')
    data = user.objects.filter(id=config.id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data)
