from django.urls import path
from src.api.public.config import media_url
from src.api.owner import home, product, booking, auth
from src.api.owner import coupon, chat, account, report

routes = [
    path('<image_id>', media_url),

    path('api/owner/home/statistics', home.statistics),
    path('api/owner/auth/register', auth.register),
    path('api/owner/auth/login', auth.login),
    path('api/owner/auth/unlock', auth.unlock),
    path('api/owner/auth/recovery', auth.recovery),
    path('api/owner/auth/token', auth.check_token),
    path('api/owner/auth/change', auth.change),
    path('api/owner/auth/user', auth.index),

    path('api/owner/product', product.index),
    path('api/owner/product/default', product.default),
    path('api/owner/product/add', product.add),
    path('api/owner/product/edit', product.edit),
    path('api/owner/product/delete', product.delete),

    path('api/owner/coupon', coupon.index),
    path('api/owner/coupon/add', coupon.add),
    path('api/owner/coupon/edit', coupon.edit),
    path('api/owner/coupon/delete', coupon.delete),

    path('api/owner/booking', booking.index),
    path('api/owner/booking/default', booking.default),
    path('api/owner/booking/add', booking.add),
    path('api/owner/booking/edit', booking.edit),
    path('api/owner/booking/delete', booking.delete),

    path('api/owner/chat', chat.index),
    path('api/owner/chat/get', chat.get),
    path('api/owner/chat/active', chat.active),
    path('api/owner/chat/send', chat.send),
    path('api/owner/chat/delete', chat.delete),

    path('api/owner/account', account.index),
    path('api/owner/account/save', account.save),
    path('api/owner/account/password', account.password),
    path('api/owner/account/history/delete', account.delete),

    path('api/owner/report', report.index),
    path('api/owner/report/delete', report.delete),
]
