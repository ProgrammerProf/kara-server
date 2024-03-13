from django.urls import path
from src.api.public.config import media_url
from src.api.guest import home, product, booking, auth
from src.api.guest import coupon, chat, account

routes = [
    path('<image_id>', media_url),
    path('api/guest/home', home.index),

    path('api/guest/auth/register', auth.register),
    path('api/guest/auth/login', auth.login),
    path('api/guest/auth/unlock', auth.unlock),
    path('api/guest/auth/recovery', auth.recovery),
    path('api/guest/auth/token', auth.check_token),
    path('api/guest/auth/change', auth.change),
    path('api/guest/auth/user', auth.index),

    path('api/guest/product', product.index),
    path('api/guest/coupon', coupon.index),
    path('api/guest/booking', booking.index),

    path('api/guest/chat', chat.index),
    path('api/guest/chat/get', chat.get),
    path('api/guest/chat/active', chat.active),
    path('api/guest/chat/send', chat.send),
    path('api/guest/chat/delete', chat.delete),

    path('api/guest/account', account.index),
    path('api/guest/account/save', account.save),
    path('api/guest/account/password', account.password),
    path('api/guest/account/history/delete', account.delete),
]
