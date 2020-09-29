from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage

def send_email(current_site,user,name):
    mail_subject = 'Activate your account.'
    message = render_to_string('Users/acc_active_email.html', {
        'user': user,
        'name': name, 
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
    email.send()