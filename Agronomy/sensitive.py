import os

from dotenv import load_dotenv


def selfDecode(_key_):
    _check_ = False
    _en_ = ''
    for _iterator_ in _key_:
        if ord(_iterator_) == 124:
            _check_ = True
            continue
        if _check_:
            _en_ += _iterator_
            _check_ = False
            continue
        _code_ = ord(_iterator_) - 5
        _en_ += (chr(_code_))
    # print(_en_)
    return _en_


load_dotenv()

SECRET_KEY = selfDecode(os.environ['SECRET_KEY'])

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
ALLOWED_DOMAIN = ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']
DATABASES = {
    'default': {
        'ENGINE': os.environ['DATABASES_DEFAULT_ENGINE'],
        'NAME': os.environ['DATABASES_DEFAULT_NAME'],
        'CLIENT':
            {
                'host': os.environ['DATABASES_DEFAULT_CLIENT_HOST'],
            }
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ['REDIS_HOST']],
        },
    },
}

'''
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
'''

# Google reCAPTCHA
# v2
RECAPTCHA_V2_SITE_KEY = os.environ['RECAPTCHA_V2_SITE_KEY']
RECAPTCHA_V2_SECRET_KEY = os.environ['RECAPTCHA_V2_SECRET_KEY']

# v3
RECAPTCHA_V3_SITE_KEY = os.environ['RECAPTCHA_V3_SITE_KEY']
RECAPTCHA_V3_SECRET_KEY = os.environ['RECAPTCHA_V3_SECRET_KEY']

# SMTP Email Configuration
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
