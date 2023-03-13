from django.shortcuts import render
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation


# Create your views here.
def setLanguage(request, language):
    view = None
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response


def indexPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'index.html', context)


def featuresPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'features.html', context)


def aboutPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'about.html', context)


def pricingPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'pricing.html', context)


def contactsPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'contacts.html', context)


def testimonialsPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'testimonials.html', context)


def faqPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'faq.html', context)


def loginPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'login.html', context)


def signupPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'signup.html', context)


def forgottenPasswordPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'forgotten-password.html', context)

