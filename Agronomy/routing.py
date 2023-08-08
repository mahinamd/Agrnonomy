from django.urls import path

from pages.consumers import ChatExpert, ChatAI

websocket_urlpatterns = [
    path('chat/room/<int:room_id>', ChatExpert.as_asgi()),
    path('en/chat/room/<int:room_id>', ChatExpert.as_asgi()),
    path('chat/ai/room/<int:room_id>', ChatAI.as_asgi()),
    path('en/chat/ai/room/<int:room_id>', ChatAI.as_asgi()),
]
