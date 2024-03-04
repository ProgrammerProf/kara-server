from src.api.public.main import *

@auth_super
def index(request, usr):
    data = setting.objects.filter(active=True).values().first()
    payments = [ch for ch in payment.objects.filter(active=True).values()]
    return response(settings=data, payments=payments)

@auth_super
def save(request, usr):
    config = setting.objects.filter(active=True).first()
    if not config: return response()
    config.name = request.POST.get('name')
    config.email = request.POST.get('email')
    config.phone = request.POST.get('phone')
    config.language = request.POST.get('language')
    config.location = request.POST.get('location')
    config.whatsapp = request.POST.get('whatsapp')
    config.facebook = request.POST.get('facebook')
    config.linkedin = request.POST.get('linkedin')
    config.youtube = request.POST.get('youtube')
    config.twitter = request.POST.get('twitter')
    config.telegram = request.POST.get('telegram')
    config.save()
    return response(status=True)

@auth_super
def option(request, usr):
    config = setting.objects.filter(active=True).first()
    if not config: return response(status=False)
    config.theme = request.POST.get('theme')
    config.mails = bool(request.POST.get('mails'))
    config.chats = bool(request.POST.get('chats'))
    config.notifications = bool(request.POST.get('notifications'))
    config.admin_register = bool(request.POST.get('admin_register'))
    config.admin_login = bool(request.POST.get('admin_login'))
    config.user_register = bool(request.POST.get('user_register'))
    config.user_login = bool(request.POST.get('user_login'))
    config.add_categories = bool(request.POST.get('add_categories'))
    config.add_products = bool(request.POST.get('add_products'))
    config.add_coupons = bool(request.POST.get('add_coupons'))
    config.add_bookings = bool(request.POST.get('add_bookings'))
    config.allow_products = bool(request.POST.get('allow_products'))
    config.allow_coupons = bool(request.POST.get('allow_coupons'))
    config.allow_bookings = bool(request.POST.get('allow_bookings'))
    config.withdraws = bool(request.POST.get('withdraws'))
    config.deposits = bool(request.POST.get('deposits'))
    config.running = bool(request.POST.get('running'))
    config.save()
    return response(status=True)

@auth_super
def payments(request, usr):
    id = integer(request.POST.get('id'))
    config = payment.objects.filter(id=id, active=True).first()
    if not config: return response()
    config.name = request.POST.get('name')
    config.email = request.POST.get('email')
    config.secret = request.POST.get('secret')
    config.date = request.POST.get('date')
    config.address = request.POST.get('address')
    config.save()
    return response(status=True)

@auth_super
def delete(request, usr):
    item = request.POST.get('item')
    if item == 'reports': action.objects.all().delete()
    if item == 'coupons': coupon.objects.all().delete()
    if item == 'bookings': booking.objects.all().delete()
    if item == 'payouts': payout.objects.all().delete()
    if item == 'categories':
        category.objects.all().delete()
        remove_file('category', True)
    if item == 'products':
        product.objects.all().delete()
        remove_file('product', True)
    if item == 'mails':
        mail.objects.all().delete()
        remove_file('mail', True)
    if item == 'chats':
        relation.objects.all().delete()
        chat.objects.all().delete()
        remove_file('chat', True)
    if item == 'supervisors':
        data = user.objects.filter(role=1, supervisor=True, super=False)
        for ch in data:
            remove_file(f'user/{ch.image}')
            ch.delete()
    if item == 'admins':
        data = user.objects.filter(role=1, supervisor=False, super=False)
        for ch in data:
            remove_file(f'user/{ch.image}')
            ch.delete()
    if item == 'owners':
        data = user.objects.filter(role=2)
        for ch in data:
            remove_file(f'user/{ch.image}')
            ch.delete()
    if item == 'guests':
        data = user.objects.filter(role=3)
        for ch in data:
            remove_file(f'user/{ch.image}')
            ch.delete()
    return response(status=True)

def default_data():
    try:
        if user.objects.filter(super=True).exists(): return
    except: return
    user(
        name='Coding Master', email='codingmaster@gmail.com',
        phone='+201099188572', country='Egytp', city='Benha',
        street='Egypt - Benha - city star', age=22, password='codingmaster',
        language='ar', currency='sar',
        create_date=get_date(), update_date=get_date(), login_date=get_date(),
        chat=True, mail=True, statistics=True, notifications=True,
        see_categories=True, add_categories=True, delete_categories=True,
        see_products=True, add_products=True, delete_products=True,
        see_bookings=True, add_bookings=True, delete_bookings=True,
        see_coupons=True, add_coupons=True, delete_coupons=True,
        see_owners=True, add_owners=True, delete_owners=True,
        see_guests=True, add_guests=True, delete_guests=True,
        control_owners_balance=True, control_guests_balance=True,
        allow_products=True, allow_bookings=True, allow_coupons=True,
        role=1, super=True, supervisor=True, active=True,
    ).save()
    setting(
        name='Coding Master', email='codingmaster@gmail.com', phone='+201099188572',
        location='Egypt - Benha - city star', language='en',
        whatsapp='+2001221083507', telegram='codingmaster001', twitter='https://twitter.com',
        facebook='https://facebook.com', youtube='https://youtube.com', instagram='https://instagram.com',
        linkedin='https://linkedin.com', theme='light',
    ).save()
    payment(name='', email='', address='', date=get_date('date'), secret='').save()
    payment(name='', email='', address='', date=get_date('date'), secret='').save()
    return True

default_data()
