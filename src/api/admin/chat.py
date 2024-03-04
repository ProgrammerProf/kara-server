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
    }
    return data

def message_data(msg):
    if not msg: return {}
    data = {
        'id': msg.id,
        'sender': msg.sender,
        'receiver': msg.receiver,
        'type': msg.type,
        'content': msg.content,
        'name': msg.name,
        'size': msg.size,
        'date': msg.date,
        'active': msg.see_receiver,
    }
    return data

@auth_admin
def index(request, usr):
    if not usr.chat: return response()
    relations = relation.objects.filter(Q(person_1=1, remove_1=False)|Q(person_2=1, remove_2=False))
    contacts = []
    for ch in relations:
        second_user = ch.person_1 if ch.person_1 != 1 else ch.person_2
        config_user = user.objects.filter(id=second_user, active=True, removed=False).first()
        if not config_user: continue
        last_message = chat.objects.filter(
            Q(sender=1, receiver=second_user, remove_sender=False) |
            Q(receiver=1, sender=second_user, remove_receiver=False)
        ).last()
        data = {
            'id': ch.id,
            'date': ch.date,
            'user': user_data(config_user),
            'messages': [message_data(last_message)] if last_message else []
        }
        contacts.append(data)
    owners = [user_data(ch) for ch in user.objects.filter(active=True, removed=False, chat=True, role=2)]
    guests = [user_data(ch) for ch in user.objects.filter(active=True, removed=False, chat=True, role=3)]
    users = owners + guests
    return response(contacts=contacts, users=users)

@auth_admin
def get(request, usr):
    if not usr.chat: return response()
    id = integer(request.POST.get('id'))
    config = relation.objects.filter(
        Q(id=id, person_1=1, remove_1=False)|
        Q(id=id, person_2=1, remove_2=False)
    ).first()
    if not config: return response(messages=[])
    second_user = config.person_1 if config.person_1 != 1 else config.person_2
    messages = chat.objects.filter(
        Q(sender=1, receiver=second_user, remove_sender=False) |
        Q(receiver=1, sender=second_user, remove_receiver=False)
    )
    data = []
    for ch in messages:
        if ch.receiver == 1:
            ch.see_receiver = True
            ch.save()
        data.append(message_data(ch))
    return response(messages=data)

@auth_admin
def active(request, usr):
    if not usr.chat: return response()
    id = integer(request.POST.get('id'))
    config = relation.objects.filter(
        Q(id=id, person_1=1, remove_1=False) |
        Q(id=id, person_2=1, remove_2=False)
    ).first()
    if not config: return response()
    second_user = config.person_1 if config.person_1 != 1 else config.person_2
    messages = chat.objects.filter(
        Q(sender=1, receiver=second_user, remove_sender=False) |
        Q(receiver=1, sender=second_user, remove_receiver=False)
    )
    for ch in messages:
        if ch.receiver == 1:
            ch.see_receiver = True
            ch.save()
    return response(status=True)

@auth_admin
def send(request, usr):
    if not usr.chat: return response()
    receiver = integer(request.POST.get('receiver'))
    check_relation = relation.objects.filter(
        Q(person_1=1, person_2=receiver)|
        Q(person_2=1, person_1=receiver)
    ).first()
    if check_relation:
        check_relation.remove_1 = False
        check_relation.remove_2 = False
        check_relation.save()
    else: relation(person_1=1, person_2=receiver, date=get_date()).save()
    content = request.POST.get('content')
    name = request.POST.get('name')
    size = request.POST.get('size')
    type = request.POST.get('type')
    ext = request.POST.get('ext')
    link = upload_file(dir='chat', file=request.FILES.get('file'), ext=ext)
    chat(
        sender=1, receiver=receiver, content=content,
        name=name, size=size, type=type, link=link, date=get_date()
    ).save()
    message = message_data(chat.objects.latest('id'))
    return response(status=True, message=message)

@auth_admin
def delete(request, usr):
    if not usr.chat: return response()
    id = integer(request.POST.get('id'))
    for_all = bool(request.POST.get('for_all'))
    config = relation.objects.filter(id=id).first()
    if not config: return response()
    if config.person_1 == 1: config.remove_1 = True
    else: config.remove_2 = True
    if for_all:
        config.remove_1 = True
        config.remove_2 = True
    config.save()
    second_user = config.person_1 if config.person_1 != 1 else config.person_2
    messages = chat.objects.filter(
        Q(sender=1, receiver=second_user, remove_sender=False)|
        Q(receiver=1, sender=second_user, remove_receiver=False)
    )
    for ch in messages:
        if ch.sender == 1: ch.remove_sender = True
        else: ch.remove_receiver = True
        if for_all:
            ch.remove_sender = True
            ch.remove_receiver = True
        ch.save()
    return response(status=True)
