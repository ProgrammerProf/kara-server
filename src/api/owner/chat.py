from src.api.public.main import *

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

@auth_owner
def index(request, usr):
    if not usr.chat: return response()
    relations = relation.objects.filter(Q(person_1=usr.id, remove_1=False)|Q(person_2=usr.id, remove_2=False))
    contacts = []
    for ch in relations:
        second_user = ch.person_1 if ch.person_1 != usr.id else ch.person_2
        config_user = user.objects.filter(id=second_user, active=True, removed=False).first()
        if not config_user: continue
        last_message = chat.objects.filter(
            Q(sender=usr.id, receiver=second_user, remove_sender=False) |
            Q(receiver=usr.id, sender=second_user, remove_receiver=False)
        ).last()
        data = {
            'id': ch.id,
            'date': ch.date,
            'user': {'id': config_user.id, 'name': config_user.name, 'online': False},
            'messages': [message_data(last_message)] if last_message else []
        }
        contacts.append(data)
    return response(contacts=contacts)

@auth_owner
def get(request, usr):
    if not usr.chat: return response()
    id = integer(request.POST.get('id'))
    config = relation.objects.filter(
        Q(id=id, person_1=usr.id, remove_1=False)|
        Q(id=id, person_2=usr.id, remove_2=False)
    ).first()
    if not config: return response(messages=[])
    second_user = config.person_1 if config.person_1 != usr.id else config.person_2
    messages = chat.objects.filter(
        Q(sender=usr.id, receiver=second_user, remove_sender=False) |
        Q(receiver=usr.id, sender=second_user, remove_receiver=False)
    )
    data = []
    for ch in messages:
        if ch.receiver == usr.id:
            ch.see_receiver = True
            ch.save()
        data.append(message_data(ch))
    return response(messages=data)

@auth_owner
def active(request, usr):
    if not usr.chat: return response()
    id = integer(request.POST.get('id'))
    config = relation.objects.filter(
        Q(id=id, person_1=usr.id, remove_1=False) |
        Q(id=id, person_2=usr.id, remove_2=False)
    ).first()
    if not config: return response()
    second_user = config.person_1 if config.person_1 != usr.id else config.person_2
    messages = chat.objects.filter(
        Q(sender=usr.id, receiver=second_user, remove_sender=False) |
        Q(receiver=usr.id, sender=second_user, remove_receiver=False)
    )
    for ch in messages:
        if ch.receiver == usr.id:
            ch.see_receiver = True
            ch.save()
    return response(status=True)

@auth_owner
def send(request, usr):
    if not usr.chat: return response()
    receiver = integer(request.POST.get('receiver'))
    check_relation = relation.objects.filter(
        Q(person_1=usr.id, person_2=receiver)|
        Q(person_2=usr.id, person_1=receiver)
    ).first()
    if check_relation:
        check_relation.remove_1 = False
        check_relation.remove_2 = False
        check_relation.save()
    else: relation(person_1=usr.id, person_2=receiver, date=get_date()).save()
    content = request.POST.get('content')
    name = request.POST.get('name')
    size = request.POST.get('size')
    type = request.POST.get('type')
    ext = request.POST.get('ext')
    link = upload_file(dir='chat', file=request.FILES.get('file'), ext=ext)
    chat(
        sender=usr.id, receiver=receiver, content=content,
        name=name, size=size, type=type, link=link, date=get_date()
    ).save()
    message = message_data(chat.objects.latest('id'))
    return response(status=True, message=message)

@auth_owner
def delete(request, usr):
    if not usr.chat: return response()
    id = integer(request.POST.get('id'))
    config = relation.objects.filter(id=id).first()
    if not config: return response()
    if config.person_1 == usr.id: config.remove_1 = True
    else: config.remove_2 = True
    config.save()
    second_user = config.person_1 if config.person_1 != usr.id else config.person_2
    messages = chat.objects.filter(
        Q(sender=usr.id, receiver=second_user, remove_sender=False)|
        Q(receiver=usr.id, sender=second_user, remove_receiver=False)
    )
    for ch in messages:
        if ch.sender == usr.id: ch.remove_sender = True
        else: ch.remove_receiver = True
        ch.save()
    return response(status=True)
