from django.urls import path, re_path
from . import views


urlpatterns = [
    path('login', views.login_page, name='login'),
    path('signup', views.signup_page, name='signup'),
    path('logout', views.account_logout, name='logout'),

    path('verification/<str:uid_base64>/<str:token>', views.verification_user, name='verification'),

    path('notifications', views.notifications_page, name='notifications'),
    path('notifications/<int:notification_id>', views.notifications_page, name='notifications'),
]
