from src.api.public.main import *

def action_data(type, user_id, action_id):
    data, _user_ = {}, {}
    user_config = user.objects.filter(id=user_id).first()
    if user_config:
        _user_ = {
            'id': user_config.id,
            'name': user_config.name,
            'image': f'U{user_config.id}',
            'link': f'admins/edit/{user_config.id}' if user_config.role == 1 else f'owners/edit/{user_config.id}'
            if user_config.role == 2 else f'guests/edit/{user_config.id}'
        }
    if type.find('owner') != -1 or type.find('guest') != -1 or type.find('admin') != -1:
        config = user.objects.filter(id=action_id).first()
        if config:
            data = {
                'id': config.id, 'name': config.name,
                'link': f'admins/edit/{config.id}' if config.role == 1 else f'owners/edit/{config.id}'
                if config.role == 2 else f'guests/edit/{config.id}'
            }
    if type.find('category') != -1:
        config = category.objects.filter(id=action_id).first()
        if config: data = {'id': config.id, 'name': config.name, 'link': f'categories/edit/{config.id}'}
    if type.find('product') != -1:
        config = product.objects.filter(id=action_id).first()
        if config: data = {'id': config.id, 'name': config.name, 'link': f'properties/edit/{config.id}'}
    if type.find('coupon') != -1:
        config = coupon.objects.filter(id=action_id).first()
        if config: data = {'id': config.id, 'name': config.code, 'link': 'coupons'}
    if type.find('booking') != -1:
        config = booking.objects.filter(id=action_id).first()
        if config: data = {'id': config.id, 'name': 'Booking Url', 'link': f'bookings/edit/{config.id}'}
    data['action_id'] = action_id
    return _user_, data

@auth_admin
def index(request, usr):
    if not usr.supervisor: return response()
    data = action.objects.filter(removed=False).order_by('-id')
    items = []
    for ch in data.values():
        ch['user'], ch['item'] = action_data(ch['type'], ch['user_id'], ch['action_id'])
        items.append(ch)
    return response(data=items)

@auth_admin
def delete(request, usr):
    if not usr.supervisor: return response()
    ids = parse(request.POST.get('ids'))
    for id in ids:
        config = action.objects.filter(id=id, removed=False).first()
        if not config: continue
        config.removed = True
        config.save()
    return response(status=True)
