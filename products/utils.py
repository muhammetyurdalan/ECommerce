from django.conf import settings
from cryptography.fernet import Fernet
from jwt import encode, decode, DecodeError, ExpiredSignatureError
from django.core.mail import EmailMessage

fernet = Fernet(settings.FERNET_KEY)

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
    from graphapi.content.verify import template
    token = encode_secret(user.uuid)
    url = f"{settings.FRONTEND_URL}/reset_password/{token}/"
    subject = 'Hesap Doğrulama'
    message = template.replace("[name]", user.name).replace("[endpoint]", url)
    from_mail = settings.EMAIL_HOST_USER
    to_mail = [user.email]
    email = EmailMessage(subject, message, from_mail, to_mail)
    email.content_subtype = 'html'
    email.send()
            
            
    