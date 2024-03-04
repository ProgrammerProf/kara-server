from src.api.public.config import *

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
        id = integer(request.POST.get('user'))
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
        id = integer(request.POST.get('user'))
        _user_ = user.objects.filter(id=id, role=1, super=True, active=True, removed=False).first()
        if not _user_: return response()
        return func(request, _user_, *args, **kwargs)
    return wrapper

# token
