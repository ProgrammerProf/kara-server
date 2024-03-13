from src.api.public.main import *
from src.api.public.mail import *

def generate_token(user_id):
    token = f"{token_hex()}-{abs(hash(get_date()))}"
    reset_token = reset.objects.filter(user_id=user_id).first()
    if reset_token:
        reset_token.token = token
        reset_token.date = get_date()
        reset_token.save()
    else: reset(user_id=user_id, token=token, date=get_date()).save()
    return token

@auth_owner
def index(request, usr):
    data = user.objects.filter(id=usr.id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data)

@auth_owner
def unlock(request, usr):
    password = request.POST.get('password')
    if password != usr.password: return response()
    data = user.objects.filter(id=usr.id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data)

@auth_api
def register(request):
    settings = setting.objects.filter(active=True).first()
    if not settings.user_register: return response(status='logout')
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if user.objects.filter(email=email, removed=False).exists():
        return response(status='exists')
    user(
        name=name, email=email, password=password, create_date=get_date(),
        update_date=get_date(), login_date=get_date(), ip=client(request, 'ip'),
        host=client(request, 'host'), login_ip=client(request, 'ip'),
        login_host=client(request, 'host'), role=2, statistics=True,
        notifications=True, see_products=True, add_products=True, delete_products=True,
        see_bookings=True, delete_bookings=True, see_coupons=True,
        add_coupons=True, delete_coupons=True, allow_products=True, allow_bookings=True,
        allow_coupons=True, reports=True, chat=True
    ).save()
    id = user.objects.latest('id').id
    record_action(request, user_id=id, type='register')
    data = user.objects.filter(id=id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data)

@auth_api
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    config = user.objects.filter(role=2, email=email, active=True, removed=False).first()
    if not config: return response(status='exists')
    if password != config.password: return response(status='not_match')
    settings = setting.objects.filter(active=True).first()
    if not settings.user_login: return response(status='logout')
    config.login_date = get_date()
    config.login_ip = client(request, 'ip')
    config.login_host = client(request, 'host')
    config.save()
    record_action(request, user_id=config.id, type='login')
    data = user.objects.filter(id=config.id).values().first()
    del data['password']
    data['token'] = encrypt(data['id'])
    return response(status=True, user=data)

@auth_api
def recovery(request):
    email = request.POST.get('email')
    config = user.objects.filter(role=2, email=email, active=True, removed=False).first()
    if not config: return response(status='exists')
    token = generate_token(config.id)
    kwargs = {"name": config.name, "email": config.email, "token": token}
    threading.Thread(target=recovery_mail, kwargs=kwargs).start()
    record_action(request, user_id=config.id, type='recovery_password')
    return response(status=True)

@auth_api
def check_token(request):
    recovery_token = request.POST.get('recovery_token')
    config = reset.objects.filter(token=recovery_token, active=True).first()
    if not config: return response()
    return response(status=True)

@auth_api
def change(request):
    password = request.POST.get('password')
    recovery_token = request.POST.get('recovery_token')
    token = reset.objects.filter(token=recovery_token, active=True).first()
    if not token: return response()
    config = user.objects.filter(id=token.user_id, role=2, active=True, removed=False).first()
    if not config: return response()
    config.password = password
    config.update_date = get_date()
    config.save()
    token.delete()
    record_action(request, user_id=config.id, type='change_password')
    return response(status=True)
