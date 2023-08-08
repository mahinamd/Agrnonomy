"""
ASGI config for Agronomy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from dotenv import load_dotenv
from .routing import websocket_urlpatterns

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agronomy.production' if os.environ['PRODUCTION'] == 'Yes' else 'Agronomy.settings')

# application = get_asgi_application()
asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    )
})

'''
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        websocket_urlpatterns
    )
})
'''
