from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from secrets import token_hex
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from project.settings import BASE_DIR
from datetime import datetime
import socket, random, os, json, datetime as dt
import shutil, base64, mimetypes, calendar, threading
from app.models import *

def media_url(request, image_id):
    if len(str(image_id)) < 2: return response()
    path = ''
    symbol, id = str(image_id)[0].lower(), integer(str(image_id)[1:])
    if symbol == 'u':
        item = user.objects.filter(id=id).first()
        if item: path = f'user/{item.image}'
    elif symbol == 'c':
        item = category.objects.filter(id=id).first()
        if item: path = f'category/{item.image}'
    elif symbol == 'h':
        item = chat.objects.filter(id=id).first()
        if item: path = f'chat/{item.link}'
    elif symbol == 'm':
        item = file.objects.filter(id=id).first()
        if item: path = f'mail/{item.link}'
    elif symbol == 'p':
        item = file.objects.filter(id=id).first()
        if item: path = f'product/{item.link}'
    if not path: return response()
    try:
        if not path: return response()
        img = open(f'{BASE_DIR}/src/media/{path}', 'rb')
        return FileResponse(img)
    except: ...
    return response()

def response(**data):
    return JsonResponse(data or {'status': False})

def upload_files(request, id=0, dir='product'):
    length = integer(request.POST.get('files_length'))
    deleted = parse(request.POST.get('deleted_files'))
    for ch in range(length):
        f = request.FILES.get(f'file_{ch}')
        type = request.POST.get(f'file_{ch}_type')
        name = request.POST.get(f'file_{ch}_name')
        size = request.POST.get(f'file_{ch}_size')
        ext = request.POST.get(f'file_{ch}_ext')
        link = upload_file(dir=dir, file=f, ext=ext)
        if dir == 'product': file(product_id=id, name=name, type=type, size=size, link=link, date=get_date()).save()
        if dir == 'mail': file(mail_id=id, name=name, type=type, size=size, link=link, date=get_date()).save()
        if dir == 'article': file(article_id=id, name=name, type=type, size=size, link=link, date=get_date()).save()
    for ch in deleted:
        f = file.objects.filter(id=ch).first()
        if not f: continue
        remove_file(f'{dir}/{f.link}')
        f.delete()
    return True

def client(request, query=""):
    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.',)
    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)): proxies.pop(0)
        if len(proxies) > 0: ip = proxies[0]
    if query == "ip": return ip
    if query == "host": return socket.gethostname()
    return ''

def random_string(length=1):
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    randome_id = ""
    for ch in range(length):
        char = random.choice([ch for ch in string])
        while char in randome_id: char = random.choice([ch for ch in string])
        randome_id += char
    return randome_id

def list_dir(path):
    try: os.mkdir(path)
    except: ...
    if os.path.exists(path):
        return os.listdir(path)
    return []

def write(path, file):
    try:
        data = file.read()
        File = open(path, "wb+")
        File.write(data)
        File.close()
    except: return False
    return True

def mk_dir(dir, date=False):
    if date: dir += f"/{get_date('year')}/{get_date('month')}/{get_date('day')}"
    dirs = dir.replace("\\", "/").replace("//", "/").split("/")
    dir = ""
    for ch in range(len(dirs)):
        if not dirs[ch]: continue
        dir += dirs[ch] if ch == 0 else f"/{dirs[ch]}"
        if not os.path.exists(dir):
            try: os.mkdir(dir)
            except: ...
    return dir

def image_ext(ext):
    list_ = [
        "png", "jpg", "jpeg", "gif", "svg", "apng",
        "avif", "jfif", "pjpeg", "pjp", "webp", "bmp", "eps"
    ]
    return ext if ext in list_ else "png"

def new_file(dir):
    List = [int(ch.split(".")[0]) for ch in list_dir(dir) if str(ch.split(".")[0]).isdigit()]
    if not List: return 1
    return max(List) + 1

def upload_file(**keys):
    file = keys.get("file")
    if not file: return
    dir = f"{BASE_DIR}/src/media/{keys.get('dir')}"
    dir = mk_dir(dir, True)
    path = f"{dir}/{new_file(dir)}.{keys.get('ext') or 'png'}"
    if not write(path, file): file = ''
    else: file = path.split(f"{keys.get('dir')}/")[-1]
    return file

def remove_file(file, rm_dir=False):
    file = f"{BASE_DIR}/src/media/{file}"
    try: os.remove(file)
    except: ...
    try:
        if rm_dir: shutil.rmtree(file)
        else:
            for ch in os.listdir(file):
                try: os.remove(f"{file}/{ch}")
                except: ...
                try: shutil.rmtree(f"{file}/{ch}")
                except: ...
    except: ...
    return True

def get_date(query="", sep="-"):
    query = query.lower()
    Months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if query == "year": return datetime.now().year
    if query == "month": return datetime.now().month
    if query == "day": return datetime.now().day
    if query == "hour": return datetime.now().hour
    if query == "minute": return datetime.now().minute
    if query == "second": return datetime.now().second
    if query == "p": return datetime.now().strftime("%p")
    if query == "week_day": return datetime.today().weekday()
    if query == "day_name": return Days[datetime.today().weekday()]
    if query == "month_name": return Months[datetime.now().month - 1]
    if query == "day_list": return Days
    if query == "days_number": return [0, 1, 2, 3, 4, 5, 6]
    if query == "day_number": return datetime.now().weekday()
    if query == "month_list": return Months
    if query == "month_days": return calendar.monthrange(datetime.now().year, datetime.now().month)[1]
    if query == "date": return datetime.now().strftime(f"%Y{sep}%m{sep}%d")
    if query == "time": return datetime.now().strftime(f"%H:%M:%S")
    return datetime.now().strftime(f"%Y{sep}%m{sep}%d %H:%M:%S")

def day_number(day):
    days = [sw.lower() for sw in get_date("day_list")]
    number = -1
    for index, ch in enumerate(days):
        if ch.find(day[:3].lower()) != -1: number = index
    return number

def fix_date(date="", sep="-"):
    if not date: return get_date()
    date_time, time = date.split(" "), ""
    if len(date_time) > 1: date, time = date_time[0], date_time[1]
    if not date: date = datetime.now().strftime(f"%Y{sep}%m{sep}%d")
    date = date.split(sep)
    if len(date) == 1: date = datetime.now().strftime(f"{date[0]}{sep}%m{sep}%d")
    elif len(date) == 2: date = datetime.now().strftime(f"{date[0]}{sep}{date[1]}{sep}%d")
    else: date = sep.join(date)
    if not time: time = datetime.now().strftime(f"%H:%M:%S")
    time = time.split(":")
    if len(time) == 1: time = datetime.now().strftime(f"{time[0]}:%M:%S")
    elif len(time) == 2: time = datetime.now().strftime(f"{time[0]}:{time[1]}:%S")
    else: time = ":".join(time)
    return f"{date} {time}"

def diff_date(start="", end="", sep="-"):
    start = fix_date(start, sep)
    end = fix_date(end, sep)
    start = datetime.now().strptime(start, f"%Y{sep}%m{sep}%d %H:%M:%S")
    end = datetime.now().strptime(end, f"%Y{sep}%m{sep}%d %H:%M:%S")
    days = (end - start).days
    seconds = (end - start).seconds
    diff = days * 24 * 60 * 60 + seconds
    return diff

def add_more_date(date="", seconds=0):
    if not seconds: return date
    date = str(date)
    if not date: date = get_date()
    if len(date.split(" ")) < 2: date = f"{get_date('date')} {date}"
    start_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_date += dt.timedelta(seconds=seconds)
    return str(start_date)

def remove_chars(text, *chars):
    text = str(text)
    for ch in chars:
        text = text.replace(ch, "")
    return text

def file_info(file, query=""):
    if not os.path.exists(file): return False
    if not os.path.isfile(file): return False
    query = query.lower().strip()
    size = os.path.getsize(file)
    edit_date = os.path.getmtime(file)
    edit_date = str(datetime.fromtimestamp(edit_date)).split(".")[0]
    if query == "size": return size
    if query == "edit_date": return edit_date
    if query == "dir": return os.path.dirname(file)
    if query == "type":
        if mimetypes.guess_type(file)[0]:
            return mimetypes.guess_type(file)[0].split("/")[0]
        else: return None
    return False

def big_number(number):
    number = list(reversed([ch for ch in str(number)]))
    new_number = ""
    for ch in range(len(number)):
        if ch % 3 == 0 and ch != 0:
            new_number += ","
        new_number += number[ch]
    new_number = "".join(reversed([ch for ch in new_number]))
    return new_number

def bool(word):
    agree = ["true", "t", "y", "yes", "1", "done", "always", "yep", "ya", "on"]
    if str(word).lower() in agree: return True
    return False

def integer(number):
    try: return int(number)
    except: ...
    return 0

def double(number, fixed=0):
    result = 0.0
    try:
        result = float(number)
        if fixed: result = round(result, fixed)
    except: ...
    return result

def parse(data):
    try: return json.loads(data)
    except: ...
    return []
