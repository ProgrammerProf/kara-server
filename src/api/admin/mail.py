from src.api.public.main import *

def user_data(_user_):
    if not _user_: return {}
    data = {
        'id': _user_.id,
        'name': _user_.name,
        'email': _user_.email,
        'create_date': _user_.create_date,
        'online': False,
        'balance': _user_.balance,
        'role': _user_.role,
        'super': _user_.super,
        'supervisor': _user_.supervisor,
    }
    return data

def mail_data(_mail_, type):
    if not _mail_: return {}
    config = _mail_
    sender = user.objects.filter(id=config.sender, removed=False).first()
    receiver = user.objects.filter(id=config.receiver, removed=False).first()
    files = file.objects.filter(mail_id=config.id)
    data = {
        'id': config.id,
        'title': config.title,
        'description': config.description,
        'content': config.content,
        'date': config.date,
        'sender': user_data(sender),
        'receiver': user_data(receiver),
        'active': config.see_sender if type == 'send' else config.see_receiver,
        'star': config.star_sender if type == 'send' else config.star_receiver,
        'important': config.important_sender if type == 'send' else config.important_receiver,
        'type': type,
        'files': [{'id': f.id, 'name': f.name, 'size': f.size, 'type': f.type} for f in files]
    }
    return data

@auth_admin
def index(request, usr):
    if not usr.mail: return response()
    all_inbox = mail.objects.filter(receiver=usr.id, remove_receiver=False).exclude(sender=usr.id).order_by('-id')
    all_send = mail.objects.filter(sender=usr.id, remove_sender=False).order_by('-id')
    inbox = [mail_data(item, 'inbox') for item in all_inbox]
    send = [mail_data(item, 'send') for item in all_send]
    users = user.objects.filter(active=True, removed=False, role=1, mail=True).exclude(id=usr.id).order_by('-id')
    users = [user_data(item) for item in users]
    return response(inbox=inbox, send=send, users=users)

@auth_admin
def send(request, usr):
    if not usr.mail: return response()
    title = request.POST.get('title')
    description = request.POST.get('description')
    content = request.POST.get('content')
    receiver = integer(request.POST.get('receiver'))
    mail(
        title=title, description=description, content=content,
        sender=usr.id, receiver=receiver, date=get_date(),
    ).save()
    latest_mail = mail.objects.latest('id')
    upload_files(request, latest_mail.id, 'mail')
    return response(status=True, mail=mail_data(latest_mail, 'send'))

@auth_admin
def actions(request, usr):
    if not usr.mail: return response()
    ids = parse(request.POST.get('ids'))
    action = request.POST.get('action')
    for id in ids:
        config = mail.objects.filter(id=id).first()
        if not config: continue
        if action == 'readen':
            if config.sender == usr.id: config.see_sender = True
            else: config.see_receiver = True
        if action == 'unread':
            if config.sender == usr.id: config.see_sender = False
            else: config.see_receiver = False
        if action == 'star':
            if config.sender == usr.id: config.star_sender = not config.star_sender
            else: config.star_receiver = not config.star_receiver
        if action == 'important':
            if config.sender == usr.id: config.important_sender = not config.important_sender
            else: config.important_receiver = not config.important_receiver
        config.save()
    return response(status=True)

@auth_admin
def delete(request, usr):
    if not usr.mail: return response()
    ids = parse(request.POST.get('ids'))
    for id in ids:
        config = mail.objects.filter(id=id).first()
        if not config: continue
        if config.sender == usr.id:
            config.remove_sender = True
            config.see_sender = True
        else:
            config.remove_receiver = True
            config.see_receiver = True
        config.save()
        if (config.remove_sender and config.remove_receiver) or \
            (config.remove_sender and config.receiver == usr.id):
            files = file.objects.filter(mail_id=config.id)
            for f in files:
                remove_file(f'mail/{f.link}')
                f.delete()
            # config.delete()
    return response(status=True)
