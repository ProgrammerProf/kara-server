from django.db import models

class user(models.Model):
    admin_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    age = models.FloatField(default=0)
    salary = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    visitors = models.IntegerField(default=0)
    orders = models.IntegerField(default=0)
    confirmed = models.IntegerField(default=0)
    cancelled = models.IntegerField(default=0)
    ip = models.CharField(max_length=255, null=True, blank=True)
    host = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.CharField(max_length=255, null=True, blank=True)
    login_date = models.CharField(max_length=255, null=True, blank=True)
    update_date = models.CharField(max_length=255, null=True, blank=True)
    removed_date = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    role = models.IntegerField(default=1)
    super = models.BooleanField(default=False)
    supervisor = models.BooleanField(default=False)
    chat = models.BooleanField(default=False)
    mail = models.BooleanField(default=False)
    statistics = models.BooleanField(default=False)
    notifications = models.BooleanField(default=True)
    see_categories = models.BooleanField(default=False)
    add_categories = models.BooleanField(default=False)
    delete_categories = models.BooleanField(default=False)
    see_products = models.BooleanField(default=False)
    add_products = models.BooleanField(default=False)
    delete_products = models.BooleanField(default=False)
    see_bookings = models.BooleanField(default=False)
    add_bookings = models.BooleanField(default=False)
    delete_bookings = models.BooleanField(default=False)
    see_coupons = models.BooleanField(default=False)
    add_coupons = models.BooleanField(default=False)
    delete_coupons = models.BooleanField(default=False)
    see_owners = models.BooleanField(default=False)
    add_owners = models.BooleanField(default=False)
    delete_owners = models.BooleanField(default=False)
    see_guests = models.BooleanField(default=False)
    add_guests = models.BooleanField(default=False)
    delete_guests = models.BooleanField(default=False)
    control_owners_balance = models.BooleanField(default=False)
    control_guests_balance = models.BooleanField(default=False)
    allow_products = models.BooleanField(default=False)
    allow_bookings = models.BooleanField(default=False)
    allow_coupons = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)

class relation(models.Model):
    person_1 = models.IntegerField(default=0)
    person_2 = models.IntegerField(default=0)
    date = models.CharField(max_length=255, null=True, blank=True)
    remove_1 = models.BooleanField(default=False)
    remove_2 = models.BooleanField(default=False)

class chat(models.Model):
    sender = models.IntegerField(default=0)
    receiver = models.IntegerField(default=0)
    type = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    remove_sender = models.BooleanField(default=False)
    remove_receiver = models.BooleanField(default=False)
    see_sender = models.BooleanField(default=True)
    see_receiver = models.BooleanField(default=False)

class mail(models.Model):
    sender = models.IntegerField(default=0)
    receiver = models.IntegerField(default=0)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    see_sender = models.BooleanField(default=True)
    see_receiver = models.BooleanField(default=False)
    important_sender = models.BooleanField(default=False)
    star_sender = models.BooleanField(default=False)
    important_receiver = models.BooleanField(default=False)
    star_receiver = models.BooleanField(default=False)
    remove_sender = models.BooleanField(default=False)
    remove_receiver = models.BooleanField(default=False)

class file(models.Model):
    mail_id = models.IntegerField(default=0)
    product_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)

class setting(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    balance = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    income = models.FloatField(default=0)
    expenses = models.FloatField(default=0)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    whatsapp = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    youtube = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    theme = models.CharField(max_length=255, null=True, blank=True)
    mails = models.BooleanField(default=True)
    chats = models.BooleanField(default=True)
    admin_register = models.BooleanField(default=True)
    user_register = models.BooleanField(default=True)
    admin_login = models.BooleanField(default=True)
    user_login = models.BooleanField(default=True)
    notifications = models.BooleanField(default=True)
    add_categories = models.BooleanField(default=True)
    add_products = models.BooleanField(default=True)
    add_bookings = models.BooleanField(default=True)
    add_coupons = models.BooleanField(default=True)
    add_users = models.BooleanField(default=True)
    allow_products = models.BooleanField(default=True)
    allow_bookings = models.BooleanField(default=True)
    allow_coupons = models.BooleanField(default=True)
    withdraws = models.BooleanField(default=True)
    deposits = models.BooleanField(default=True)
    running = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

class payment(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    secret = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

class category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    create_date = models.CharField(max_length=255, null=True, blank=True)
    update_date = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    allow_products = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

class product(models.Model):
    category_id = models.IntegerField(default=0)
    owner_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.CharField(max_length=255, null=True, blank=True)
    update_date = models.CharField(max_length=255, null=True, blank=True)
    removed_date = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    availability = models.TextField(null=True, blank=True)
    policy = models.TextField(null=True, blank=True)
    rules = models.TextField(null=True, blank=True)
    safety = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    old_price = models.FloatField(default=0)
    new_price = models.FloatField(default=0)
    adults = models.IntegerField(default=0)
    rooms = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    beds = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    bookings = models.IntegerField(default=0)
    rate = models.FloatField(default=0)

    desert_view = models.BooleanField(default=True)
    sea_view = models.BooleanField(default=True)
    hair_dryer = models.BooleanField(default=True)
    cleaning_properties = models.BooleanField(default=True)
    washing_machine = models.BooleanField(default=True)
    iron = models.BooleanField(default=True)
    indoor_stove = models.BooleanField(default=True)
    wifi = models.BooleanField(default=True)
    kitchen = models.BooleanField(default=True)
    refrigerator = models.BooleanField(default=True)
    oven = models.BooleanField(default=True)
    television = models.BooleanField(default=True)
    air_conditioner = models.BooleanField(default=True)
    dining_table = models.BooleanField(default=True)
    ceiling_fan = models.BooleanField(default=True)
    desk_fan = models.BooleanField(default=True)
    necessities = models.BooleanField(default=True)
    allow_bookings = models.BooleanField(default=True)
    cancellation = models.BooleanField(default=True)
    pay_later = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)

class booking(models.Model):
    admin_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    product_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    create_date = models.CharField(max_length=255, null=True, blank=True)
    update_date = models.CharField(max_length=255, null=True, blank=True)
    removed_date = models.CharField(max_length=255, null=True, blank=True)
    booking_date = models.CharField(max_length=255, null=True, blank=True)
    coupon = models.CharField(max_length=255, null=True, blank=True)
    paid = models.BooleanField(default=False)
    status = models.IntegerField(default=1)
    remove_user = models.BooleanField(default=False)
    remove_owner = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)

class coupon(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    discount = models.FloatField(default=0)
    uses = models.IntegerField(default=0)
    create_date = models.CharField(max_length=255, null=True, blank=True)
    update_date = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

class reset(models.Model):
    user_id = models.IntegerField(default=0)
    token = models.TextField(null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

class payout(models.Model):
    user_id = models.IntegerField(default=0)
    tour_id = models.IntegerField(default=0)
    order_id = models.IntegerField(default=0)
    adults = models.IntegerField(default=0)
    real_price = models.FloatField(default=0)
    paid_price = models.FloatField(default=0)
    paid_secret = models.CharField(max_length=255, null=True, blank=True)
    paid_date = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True)

class action(models.Model):
    user_id = models.IntegerField(default=0)
    action_id = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    type = models.CharField(max_length=255, null=True, blank=True)
    secret = models.CharField(max_length=255, null=True, blank=True)
    ip = models.CharField(max_length=255, null=True, blank=True)
    host = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)
    # register
    # login
    # deposit
    # withdraw
    # confirm_withdraw
    # send_mail
    # send_message
    # delete_mail
    # delete_chat
    # edit_account
    # change_password
    # edit_setting
    # edit_payment
    # delete_setting-products
    # create_category
    # edit_category
    # delete_category
    # create_product
    # edit_product
    # delete_product
    # create_coupon
    # edit_coupon
    # delete_coupon
    # create_booking
    # edit_booking
    # delete_booking
    # confirm_booking
    # cancel_booking
    # create_admin
    # edit_admin
    # delete_admin
    # create_owner
    # edit_owner
    # delete_owner
    # create_guest
    # edit_guest
    # delete_guest
