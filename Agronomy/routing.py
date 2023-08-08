import os

from dotenv import load_dotenv
from django.core.asgi import get_asgi_application
from django.urls import path
from pages.consumers import ChatExpert, ChatAI

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agronomy.production' if os.environ['PRODUCTION'] == 'Yes' else 'Agronomy.settings')

asgi_application = get_asgi_application()

websocket_urlpatterns = [
    path('chat/room/<int:room_id>', ChatExpert.as_asgi()),
    path('en/chat/room/<int:room_id>', ChatExpert.as_asgi()),
    path('chat/ai/room/<int:room_id>', ChatAI.as_asgi()),
    path('en/chat/ai/room/<int:room_id>', ChatAI.as_asgi()),
]
