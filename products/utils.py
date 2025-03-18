import json
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from cryptography.fernet import Fernet
from jinja2 import Environment, FileSystemLoader
from jwt import encode, decode, DecodeError, ExpiredSignatureError
from django.core.mail import EmailMessage

fernet = Fernet(settings.FERNET_KEY)
templates_env = Environment(loader=FileSystemLoader('graphapi/templates'))

def set_attributes(instance, data, exclude=[]):
    for key in data:
        if key in exclude:
            continue
        value = data.get(key)
        if value is not None:
            setattr(instance, key, value)
            
            
def encode_secret(payload):
    secret, algorithm = settings.JWT_SECRET, settings.JWT_ALGORITHM
    token = encode(payload, secret, algorithm)
    secret = fernet.encrypt(token.encode()).decode()
    return secret


def decode_secret(secret):
    token = fernet.decrypt(secret.encode()).decode()
    try:
        data = decode(token, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
    except DecodeError:
        raise Exception("Invalid token")
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    return data

            
def send_verify_mail(user):
    template = templates_env.get_template('verify.html')
    payload = {
        'uuid': str(user.uuid),
        'exp': timezone.now() + timedelta(minutes=10),
    }
    token = encode_secret(payload)
    url = f"{settings.BACKEND_URL}/verify_user/{token}/"
    subject = 'Hesap Doğrulama'
    data = {
        "name": user.name,
        "endpoint": url
    }
    message = template.render(data=data)
    from_mail = settings.EMAIL_HOST_USER
    to_mail = [user.email]
    email = EmailMessage(subject, message, from_mail, to_mail)
    email.content_subtype = 'html'
    email.send()
            
    