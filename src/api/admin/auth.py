from src.api.public.main import *

@auth_admin
def index(request, usr):
    config = user.objects.filter(id=usr.id, active=True, removed=False, role=1).values().first()
    if not config: return response()
    del config['password']
    return response(status=True, user=config)

@auth_admin
def unlock(request, usr):
    password = request.POST.get('password')
    config = user.objects.filter(id=usr.id, password=password, active=True, removed=False, role=1).values().first()
    if not config: return response()
    del config['password']
    return response(status=True, user=config)

@auth_api
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    config = user.objects.filter(email=email, password=password, active=True, removed=False, role=1).values().first()
    if not config: return response(status=False)
    del config['password']
    if not config['super']:
        settings = setting.objects.filter(active=True).first()
        if not settings: return response(status='logout')
        if not settings.admin_login: return response(status='logout')
    return response(status=True, user=config)
