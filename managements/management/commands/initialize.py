import django
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        django.setup(set_prefix=False)
