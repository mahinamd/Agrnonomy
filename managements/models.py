import os

from django.conf import settings
from django.db import models
from djongo import models as djongo_models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from accounts.models import remove_temp_files


# Supporting functions
def get_default_img_filepath():
    return "default/cloud_upload.png"


# Category model
def get_category_img_filepath(self, filename):
    remove_temp_files("category_img")
    return "category_img/temp_category_img." + filename.split('.')[-1]


class Category(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    image = models.ImageField(verbose_name='Image', max_length=255, null=False, blank=False, default=get_default_img_filepath, upload_to=get_category_img_filepath)
    name_bn = models.CharField(verbose_name="Name (bn)", max_length=255, null=False, blank=False)
    name_en = models.CharField(verbose_name="Name (en)", max_length=255, null=False, blank=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Categories"


# Subcategory model
def get_subcategory_img_filepath(self, filename):
    remove_temp_files("subcategory_img")
    return "subcategory_img/temp_subcategory_img." + filename.split('.')[-1]


class Subcategory(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE, related_name='subcategories')
    image = models.ImageField(verbose_name='Image', max_length=255, null=False, blank=False, default=get_default_img_filepath, upload_to=get_subcategory_img_filepath)
    name_bn = models.CharField(verbose_name="Name (bn)", max_length=255, null=False, blank=False)
    name_en = models.CharField(verbose_name="Name (en)", max_length=255, null=False, blank=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Subcategories"


# Information model
class Information(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    subcategory = models.ForeignKey(Subcategory, null=False, blank=False, on_delete=models.CASCADE, related_name='information')
    name_bn = models.CharField(verbose_name="Name (bn)", max_length=255, null=False, blank=False)
    details_bn = models.CharField(verbose_name="Details (bn)", max_length=7650, null=False, blank=False)
    name_en = models.CharField(verbose_name="Name (en)", max_length=255, null=False, blank=False)
    details_en = models.CharField(verbose_name="Details (en)", max_length=7650, null=False, blank=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Information"


# Disease/Problem model
def get_disease_img_filepath(self, filename):
    remove_temp_files("disease_problem_img")
    return "disease_problem_img/temp_disease_problem_img." + filename.split('.')[-1]


class DiseaseProblem(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    subcategory = models.ForeignKey(Subcategory, null=False, blank=False, on_delete=models.CASCADE, related_name='disease_problem')
    image = models.ImageField(verbose_name='Image', max_length=255, null=False, blank=False, default=get_default_img_filepath, upload_to=get_disease_img_filepath)
    name_bn = models.CharField(verbose_name="Name (bn)", max_length=765, null=False, blank=False)
    insects_causes_bn = models.CharField(verbose_name="Insects/Causes (bn)", max_length=765, null=True, blank=True)
    solution_bn = models.CharField(verbose_name="Solution (bn)", max_length=765, null=True, blank=True)
    warning_bn = models.CharField(verbose_name="Warning (bn)", max_length=765, null=True, blank=True)
    name_en = models.CharField(verbose_name="Name (en)", max_length=765, null=False, blank=False)
    insects_causes_en = models.CharField(verbose_name="Insects/Causes (en)", max_length=765, null=True, blank=True)
    solution_en = models.CharField(verbose_name="Solution (en)", max_length=765, null=True, blank=True)
    warning_en = models.CharField(verbose_name="Warning (en)", max_length=765, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Diseases/Problems"


@receiver(pre_delete, sender=Category)
@receiver(pre_delete, sender=Subcategory)
@receiver(pre_delete, sender=DiseaseProblem)
def delete_image_file(sender, instance, **kwargs):
    if "default/" not in str(instance.image):
        instance.image.delete(save=False)
