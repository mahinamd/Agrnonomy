'''
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                path('ws/my_websocket/', MyConsumer.as_asgi()),
            )
        )
    ),
})
'''

from django.urls import path
from pages.expert import ChatExpert

websocket_urlpatterns = [
    path('chat/room/<int:room_id>', ChatExpert.as_asgi()),
    path('en/chat/room/<int:room_id>', ChatExpert.as_asgi()),
]
