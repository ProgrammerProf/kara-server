from src.api.public.config import *

def record_action(request, **kwargs):
    action(
        user_id=integer(kwargs.get('user_id')),
        action_id=integer(kwargs.get('action_id')),
        amount=double(kwargs.get('amount')),
        status=integer(kwargs.get('status')),
        paid=bool(kwargs.get('paid')),
        type=kwargs.get('type') or '',
        location=kwargs.get('location') or '',
        secret=kwargs.get('secret') or '',
        date=get_date(),
        ip=client(request, 'ip'),
        host=client(request, 'host'),
    ).save()
    return True

def auth_api(func):
    @csrf_exempt
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST': return response()
        return func(request, *args, **kwargs)
    return wrapper

def auth_admin(func):
    @csrf_exempt
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST': return response()
        id = integer(decrypt(request.POST.get('token')))
        _user_ = user.objects.filter(id=id, role=1, active=True, removed=False).first()
        if not _user_: return response()
        if not _user_.super:
            settings = setting.objects.filter(active=True).first()
            if not settings: return response(status='logout')
            if not settings.admin_login: return response(status='logout')
        return func(request, _user_, *args, **kwargs)
    return wrapper

def auth_super(func):
    @csrf_exempt
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST': return response()
        id = integer(decrypt(request.POST.get('token')))
        _user_ = user.objects.filter(id=id, role=1, super=True, active=True, removed=False).first()
        if not _user_: return response()
        return func(request, _user_, *args, **kwargs)
    return wrapper
