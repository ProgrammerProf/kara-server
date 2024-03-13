from src.api.public.config import *

def recovery_mail(**keywargs):
    try:
        subject= f'Kara - Reset Password'
        data = {
            'reset_link': f"auth/change/{keywargs.get('token')}",
            'username': keywargs.get('name') or 'Dear',
            'year': get_date('year'),
            'host': 'http://127.0.0.1:3000',
            'img_url': 'https://kaarra.pythonanywhere.com/media/public/',
            'subject': subject,
        }
        html_content = render_to_string('recovery_mail.html', data)
        msg = EmailMultiAlternatives(
            subject, strip_tags(html_content), 'info@kaarra.com',
            [keywargs.get('email')]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except: ...
