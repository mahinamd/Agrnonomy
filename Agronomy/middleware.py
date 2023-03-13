from django.http import HttpResponsePermanentRedirect
from .production import ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().partition(':')[0]
        if host == ALLOWED_HOSTS[0] or host == ALLOWED_HOSTS[1]:
            return HttpResponsePermanentRedirect(CSRF_TRUSTED_ORIGINS[2] + request.path)
        else:
            return self.get_response(request)
