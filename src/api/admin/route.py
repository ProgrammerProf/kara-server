from django.urls import path
from src.api.public.config import media_url
from src.api.admin import home, category, product, user, booking, auth
from src.api.admin import coupon, mail, chat, setting, account, report

routes = [
    path('<image_id>', media_url),

    path('api/admin/home/statistics', home.statistics),
    path('api/admin/auth/login', auth.login),
    path('api/admin/auth/unlock', auth.unlock),
    path('api/admin/auth/user', auth.index),

    path('api/admin/category', category.index),
    path('api/admin/category/add', category.add),
    path('api/admin/category/edit', category.edit),
    path('api/admin/category/delete', category.delete),

    path('api/admin/product', product.index),
    path('api/admin/product/default', product.default),
    path('api/admin/product/add', product.add),
    path('api/admin/product/edit', product.edit),
    path('api/admin/product/delete', product.delete),

    path('api/admin/user', user.index),
    path('api/admin/user/add', user.add),
    path('api/admin/user/edit', user.edit),
    path('api/admin/user/delete', user.delete),

    path('api/admin/coupon', coupon.index),
    path('api/admin/coupon/add', coupon.add),
    path('api/admin/coupon/edit', coupon.edit),
    path('api/admin/coupon/delete', coupon.delete),

    path('api/admin/booking', booking.index),
    path('api/admin/booking/default', booking.default),
    path('api/admin/booking/add', booking.add),
    path('api/admin/booking/edit', booking.edit),
    path('api/admin/booking/delete', booking.delete),

    path('api/admin/mail', mail.index),
    path('api/admin/mail/send', mail.send),
    path('api/admin/mail/delete', mail.delete),
    path('api/admin/mail/actions', mail.actions),

    path('api/admin/chat', chat.index),
    path('api/admin/chat/get', chat.get),
    path('api/admin/chat/active', chat.active),
    path('api/admin/chat/send', chat.send),
    path('api/admin/chat/delete', chat.delete),

    path('api/admin/setting', setting.index),
    path('api/admin/setting/save', setting.save),
    path('api/admin/setting/option', setting.option),
    path('api/admin/setting/payment', setting.payments),
    path('api/admin/setting/delete', setting.delete),

    path('api/admin/account', account.index),
    path('api/admin/account/save', account.save),
    path('api/admin/account/password', account.password),
    path('api/admin/account/history/delete', account.delete),

    path('api/admin/report', report.index),
    path('api/admin/report/delete', report.delete),
]
