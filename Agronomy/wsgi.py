"""
WSGI config for Agronomy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agronomy.production' if os.environ['PRODUCTION'] == 'Yes' else 'Agronomy.settings')

application = get_wsgi_application()
