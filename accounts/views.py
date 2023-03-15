from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Account
from .forms import (
    AccountForm, AccountUpdateForm, AccountAuthenticationForm
)
from django.utils import translation
from pages.views import setLanguage, indexPage


# Create your views here.
def get_redirect_if_exists(request):
    is_redirect = None
    if request.GET:
        if request.GET.get("next"):
            is_redirect = str(request.GET.get("next"))
    return is_redirect


def signup_view(request, *args, **kwargs):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    user = request.user
    if user.is_authenticated:
        messages.error(request, "You are already authenticated as " + str(user.email))
        return redirect('index')

    context = {}
    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            rpass = form.cleaned_data.get('mpass')
            user = authenticate(email=email, password=rpass)
            # login(request, account)
            destination = get_redirect_if_exists(request)
            # destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            messages.success(request, "Successfully Signup")
            return redirect('login')
        else:
            context['form'] = form
    else:
        form = AccountForm()
    context['form'] = form
    return render(request, 'signup.html', context)


def account_logout(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully Logged Out")
    else:
        messages.error(request, "You are already Logged Out")
    return redirect('login')


def login_view(request, *args, **kwargs):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}
    user = request.user
    if user.is_authenticated:
        messages.error(request, "You are already authenticated as " + str(user.email))
        return redirect('index')

    if request.POST:
        context = {'data': request.POST}
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            # email = request.POST['email']
            # password = request.POST['password']
            # user = authenticate(email=email, password=password)
            # token = form.cleaned_data.get('token')
            captcha = True

            if captcha:
                email = form.cleaned_data.get('email').lower()
                rpass = form.cleaned_data.get('password')
                user = authenticate(email=email, password=rpass)

                if user:
                    login(request, user)
                    remember_me = form.cleaned_data.get('rme')
                    if not remember_me:
                        request.session.set_expiry(0)
                    else:
                        request.session['uid'] = user.pk
                        request.session['uemail'] = user.email

                    destination = get_redirect_if_exists(request)
                    if destination:
                        return redirect(destination)
                    messages.success(request, "Successfully Logged In")
                    return redirect('index')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return redirect('login')
        else:
            messages.error(request, 'Please try again.')
            return redirect('login')
    else:
        form = AccountAuthenticationForm()
    context['form'] = form
    return render(request, "login.html", context)
