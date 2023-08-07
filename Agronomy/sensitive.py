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
        'ENGINE': selfDecode(os.environ['ENGINE']),
        'NAME': selfDecode(os.environ['NAME']),
        'CLIENT':
            {
                'host': selfDecode(os.environ['HOST_LINK']) + selfDecode(os.environ['HOST_PERMISSION']),
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