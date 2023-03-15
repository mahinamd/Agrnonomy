from django.shortcuts import render, HttpResponse, redirect
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.contrib import messages
from Agronomy.connection import get_collection


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
    user = request.user
    if user.is_authenticated:
        messages.error(request, "You are already authenticated as " + str(user.email))
        return redirect('index')

    return render(request, 'login.html', context)


def signupPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    user = request.user
    if user.is_authenticated:
        messages.error(request, "You are already authenticated as " + str(user.email))
        return redirect('index')

    return render(request, 'signup.html', context)


def forgottenPasswordPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    return render(request, 'forgotten-password.html', context)


def dashboardPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    user = request.user
    if user.is_authenticated and user.is_superuser:
        return render(request, 'dashboard.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect('index')


def dataManagementPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    user = request.user
    if user.is_authenticated and user.is_superuser:
        return render(request, 'data-management.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect('index')


def profilePage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    user = request.user
    if user.is_authenticated:
        return render(request, 'profile.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect('index')


def get_titles():
    context = {}
    collection = get_collection()
    data = collection.find({}, {'_id': 0, 'data': 1})

    for result in data:
        context['total_category'] = len(result['data'][0]['data_title']) - 1
        context['category_title'] = result['data'][0]['data_title']['category_title']
        context['data_title'] = [result['data'][0]['data_title']['land_title'],
                                 result['data'][0]['data_title']['seed_title'],
                                 result['data'][0]['data_title']['manure_title'],
                                 result['data'][0]['data_title']['irrigation_title'],
                                 result['data'][0]['data_title']['disease_title'],
                                 result['data'][0]['data_title']['insects_title'],
                                 result['data'][0]['data_title']['solution_title'],
                                 result['data'][0]['data_title']['warning_title']]
        break

    return context


def get_categories_title():
    collection = get_collection()
    data = collection.find({}, {'_id': 0, 'data': 1})
    categories = []

    for result in data:
        categories.append(result['data'][0]['category'])

    return categories


def get_categories_image():
    collection = get_collection()
    data = collection.find({}, {'_id': 0, 'data': 1})
    categories = []

    for result in data:
        categories.append(result['data'][0]['category_image'])

    return categories


def categoryPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    context.update(get_titles())
    categories_title = get_categories_title()
    categories_image = get_categories_image()
    categories = zip(categories_title, categories_image)
    context['categories'] = categories

    user = request.user
    if user.is_authenticated:
        return render(request, 'category.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect('index')


def informationPage(request, index):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    user = request.user
    if user.is_authenticated:
        return render(request, 'information.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect('index')
