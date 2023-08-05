from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Account, Notification
from .forms import (
    AccountForm, AccountUpdateForm, AccountAuthenticationForm
)
from django.urls.base import resolve, reverse
from django.utils import translation


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


def create_notification(request, user, account_id, notification):
    if user.is_authenticated and user and account_id:
        account = Account.objects.get(id=account_id)
        Notification.objects.create(account=account, created_by=user, notification=notification)
        messages.success(request, "The notification has been created successfully")
        return True

    messages.error(request, "You are not allow to create notification")
    return False


def notifications_page(request, notification_id=None, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.method == "GET" and notification_id and len(context) == 1:
            notification = Notification.objects.get(id=notification_id)
            filters = request.GET.get('read')
            if filters:
                if filters == "Yes" and not notification.read:
                    notification.read = True
                    notification.save()
                    messages.success(request, "The notification has been marked as read successfully")
                elif filters == "No" and notification.read:
                    notification.read = False
                    notification.save()
                    messages.success(request, "The notification has been marked as unread successfully")
                else:
                    messages.error(request, "Invalid read request, failed to mark the notification")

            return redirect(reverse('notifications'))
        else:
            notifications = Notification.objects.filter(account=user)
            notifications_count = notifications.count()
            filters = request.GET.get('read')
            if filters:
                if filters == "Mark-all":
                    flag = False
                    for notification in notifications:
                        if not notification.read:
                            notification.read = True
                            notification.save()
                            flag = True

                    if flag:
                        messages.success(request, "The notifications has been marked as read successfully")

            filters = request.GET.get('tab')
            if filters:
                filters = filters.split(',') if ',' in filters else filters
                if isinstance(filters, list) and len(filters) == 2 and "Newest" in filters and "Unread" in filters:
                    notifications = Notification.objects.filter(account=user).order_by('-timestamp')
                    notifications = [notification for notification in notifications if not notification.read]
                    notifications_count = len(notifications)
                elif filters == "Newest":
                    notifications = Notification.objects.filter(account=user).order_by('-timestamp')
                    notifications_count = notifications.count()
                elif filters == "Unread":
                    notifications = Notification.objects.filter(account=user)
                    notifications = [notification for notification in notifications if not notification.read]
                    notifications_count = len(notifications)
                else:
                    messages.error(request, "Invalid tab request, failed to load the notifications")
                    return redirect(reverse("notifications"))

            context["notifications"] = notifications
            context["notifications_count"] = notifications_count
            return render(request, 'notifications.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))
