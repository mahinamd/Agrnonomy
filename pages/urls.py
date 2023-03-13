from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.indexPage, name='index'),
    path('features', views.featuresPage, name='features'),
    path('about', views.aboutPage, name='about'),
    path('pricing', views.pricingPage, name='pricing'),
    path('contacts', views.contactsPage, name='contacts'),
    path('testimonials', views.testimonialsPage, name='testimonials'),
    path('faq', views.faqPage, name='faq'),
    path('login', views.loginPage, name='login'),
    path('signup', views.signupPage, name='signup'),
    path('forgotten-password', views.forgottenPasswordPage, name='forgotten-password'),
    path("setLanguage/<str:language>", views.setLanguage, name="set-language"),
]
