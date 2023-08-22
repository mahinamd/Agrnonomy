import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls.base import reverse
from .production import ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS

logger = logging.getLogger(__name__)


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().partition(':')[0]
        if host == ALLOWED_HOSTS[0] or host == ALLOWED_HOSTS[1]:
            return HttpResponsePermanentRedirect(CSRF_TRUSTED_ORIGINS[2] + request.path)
        else:
            return self.get_response(request)


def check_session(request):
    user = request.user
    if user.is_authenticated:
        try:
            if request.session.get('user_id') or request.session.get('_auth_user_id'):
                return 1
            else:
                request.session.flush()
                request.session.clear_expired()
                logout(request)
        except Exception as e:
            logger.error(f"Exception occurred in check session: {e}")
            return -1

    return 0


class SessionCheckerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before processing the view, check the session
        is_user_authenticated = False
        if request.user.is_authenticated:
            is_user_authenticated = True

        is_session_valid = check_session(request)
        if is_user_authenticated and is_session_valid == 0:
            messages.error(request, 'Session expired. Please login again.')
            return redirect('login')
        elif is_session_valid == -1:
            messages.error(request, 'Invalid session. Please try again.')
            return redirect('index')

        response = self.get_response(request)
        return response


class PreventGoogleOauthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/accounts/google/login/" or request.path == "/en/accounts/google/login/":
            user = request.user
            if user.is_authenticated:
                messages.error(request, "You are already authenticated as " + str(user.email))
                return redirect('index')

            referer_url = request.META.get('HTTP_REFERER')
            signup_url = request.build_absolute_uri(reverse('signup'))
            login_url = request.build_absolute_uri(reverse('login'))

            if not referer_url or ("/accounts/google/login/" in referer_url and (("/en/" in request.path and "/en/" not in referer_url) or ("/en/" not in request.path and "/en/" in referer_url))) or ("/accounts/google/login/" not in referer_url and referer_url != signup_url and referer_url != login_url):
                messages.error(request, "Invalid request for Google Oauth.")
                return redirect('index')

        return self.get_response(request)
