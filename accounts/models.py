from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone')

        user = self.model(email=self.normalize_email(email), phone=phone,)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(email=self.normalize_email(email), phone=phone, password=password,)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_pimg_filepath(self, filename):
    return 'pimg/' + str(self.pk) + '/' + str(self.pk) + '_profile.png'


def get_default_pimg():
    return '/pimg/default_profile.png'


# Create your models here.
class Account(AbstractBaseUser):
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    rme = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    phone = models.CharField(max_length=64, unique=True)
    pimg = models.ImageField(max_length=255, upload_to=get_pimg_filepath, null=True, blank=True, default=get_default_pimg)
    fname = models.CharField(max_length=32, blank=True, null=True)
    lname = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=32, blank=True, null=True)
    dob = models.DateField(default=None, blank=True, null=True)

    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=128)

    house_no = models.CharField(max_length=128, blank=True, null=True)
    address_line = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    zip_code = models.CharField(max_length=32, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)

    social_li = models.CharField(max_length=255, blank=True, null=True)
    social_fb = models.CharField(max_length=255, blank=True, null=True)
    social_tw = models.CharField(max_length=255, blank=True, null=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.phone

    def get_name(self):
        return self.fname + ' ' + self.lname

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
