from django.urls import path, re_path
from . import views


urlpatterns = [
    path('login-form', views.login_view, name='login-form'),
    path('signup-form', views.signup_view, name='signup-form'),
    path('logout', views.account_logout, name='logout'),

    path('notifications', views.notifications_page, name='notifications'),
    path('notifications/<int:notification_id>', views.notifications_page, name='notifications'),
]
