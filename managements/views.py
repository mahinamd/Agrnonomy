from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import translation
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings

from .models import Category, Subcategory, Information, DiseaseProblem
from .forms import CategoryForm, SubcategoryForm, InformationForm, DiseaseProblemForm

from accounts.models import Account
from accounts.views import create_notification
from pages.models import Room, Problem, Message
from pages.forms import RoomForm

from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
import copy
import cv2
import json
import base64
import requests
from django.core import files
import traceback
from PIL import Image
from io import BytesIO
from django.http import JsonResponse


# Supporting functions
def cropping_image(cropping_details, img_dir_filepath, img_filename, temp_img_filename, old_img_filename=None):
    if cropping_details:
        cropping_details = json.loads(cropping_details)
        x = cropping_details['x'] if cropping_details['x'] >= 0 else 0
        y = cropping_details['y'] if cropping_details['y'] >= 0 else 0
        width = cropping_details['width']
        height = cropping_details['height']

        is_renamed = False
        if old_img_filename is not None and os.path.exists(img_dir_filepath + '/' + img_filename):
            os.rename(img_dir_filepath + '/' + img_filename, img_dir_filepath + '/' + old_img_filename)
            is_renamed = True

        if os.path.exists(img_dir_filepath + '/' + temp_img_filename):
            with open(img_dir_filepath + '/' + temp_img_filename, 'rb') as f:
                original_img = Image.open(f)
                cropped_img = original_img.crop((x, y, x + width, y + height))
                cropped_img = cropped_img.convert('RGB')
                cropped_img.save(img_dir_filepath + '/' + img_filename, 'JPEG', quality=70, optimize=True)

            os.remove(img_dir_filepath + '/' + temp_img_filename)
            if is_renamed:
                os.remove(img_dir_filepath + '/' + old_img_filename)

            return True
        else:
            return False
    else:
        return False


def rollback_save(instance, img_dir_filepath, img_filename, temp_img_filename):
    if img_dir_filepath:
        if temp_img_filename and os.path.exists(img_dir_filepath + '/' + temp_img_filename):
            os.remove(img_dir_filepath + '/' + temp_img_filename)
        if img_filename and os.path.exists(img_dir_filepath + '/' + img_filename):
            os.remove(img_dir_filepath + '/' + img_filename)

    if instance:
        instance.delete()


def rollback_update(instance, old_object, form_name, img_dir_filepath, img_filename, temp_img_filename, old_img_filename):
    if img_dir_filepath:
        if img_filename and old_img_filename and os.path.exists(img_dir_filepath + '/' + old_img_filename):
            if os.path.exists(img_dir_filepath + '/' + img_filename):
                os.remove(img_dir_filepath + '/' + img_filename)
            os.rename(img_dir_filepath + '/' + old_img_filename, img_dir_filepath + '/' + img_filename)
        if temp_img_filename and os.path.exists(img_dir_filepath + "/" + temp_img_filename):
            os.remove(img_dir_filepath + '/' + temp_img_filename)

    if instance and old_object:
        instance.image = old_object.image
        instance.name_bn = old_object.name_bn
        instance.name_en = old_object.name_en
        if form_name == 'disease_problem':
            instance.insects_causes_bn = old_object.insects_causes_bn
            instance.solution_bn = old_object.solution_bn
            instance.warning_bn = old_object.warning_bn
            instance.insects_causes_en = old_object.insects_causes_en
            instance.warning_en = old_object.warning_en
            instance.solution_en = old_object.solution_en

        instance.save()


def save_form(request, form, context, form_name):
    if form.is_valid():
        instance = form.save()
        img_dir_filepath = ''
        temp_img_filename = ''
        img_filename = ''

        try:
            img_id = str(instance.id)

            original_img_file = form.cleaned_data.get('image')
            cropping_details = request.POST.get("cropping_details")

            if original_img_file and "default/" not in str(original_img_file) and cropping_details:
                img_dir_filepath = os.path.join(settings.MEDIA_ROOT, form_name + "_img")
                img_filename = img_id + '_' + form_name + "_img.jpg"
                temp_img_filename = "temp_" + form_name + "_img" + '.' + original_img_file.name.split('.')[-1]

                valid = cropping_image(cropping_details, img_dir_filepath, img_filename, temp_img_filename)

                if valid:
                    instance.image = form_name + "_img/" + img_filename
                    instance.save()
                    messages.success(request, "The " + form_name.replace('_', '/') + " has been added successfully")
                else:
                    rollback_save(instance, img_dir_filepath, img_filename, temp_img_filename)
                    messages.error(request, "Invalid image, failed to add the " + form_name.replace('_', '/'))
            elif "default/" in str(original_img_file):
                messages.success(request, "The " + form_name.replace('_', '/') + " has been added successfully")
            else:
                rollback_save(instance, img_dir_filepath, img_filename, temp_img_filename)
                messages.error(request, "Invalid request, failed to add the " + form_name.replace('_', '/'))

            return redirect(reverse("insert-" + form_name.replace('_', '-') + "-form"))

        except Exception as e:
            rollback_save(instance, img_dir_filepath, img_filename, temp_img_filename)
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()
    else:
        context['form'] = form

    messages.error(request, "Invalid request, failed to add the " + form_name.replace('_', '/'))
    if form_name == 'category':
        return insertCategoryPage(request, context)
    elif form_name == 'subcategory':
        return insertSubcategoryPage(request, context)
    elif form_name == 'disease_problem':
        return insert_disease_problem_page(request, context)
    else:
        messages.error(request, "Invalid " + form_name.replace('_', '/') + " form, try again")
        return viewCategoryPage(request)


def is_valid_list(item_list):
    if not item_list:
        return False

    for item in item_list:
        if not item or item == '' or item.isspace():
            return False

    return True


def update_form(request, context, form_name, object_id):
    update_object = None
    form = None
    if form_name == 'category':
        update_object = Category.objects.get(pk=object_id)
        form = CategoryForm(request.POST, request.FILES, instance=update_object)
    elif form_name == 'subcategory':
        update_object = Subcategory.objects.get(pk=object_id)
        form = SubcategoryForm(request.POST, request.FILES, instance=update_object)
    elif form_name == 'disease_problem':
        update_object = DiseaseProblem.objects.get(pk=object_id)
        form = DiseaseProblemForm(request.POST, request.FILES, instance=update_object)

    old_object = copy.deepcopy(update_object)
    if update_object is not None and form.is_valid():
        instance = form.save()
        img_dir_filepath = ''
        img_filename = ''
        old_img_filename = ''
        temp_img_filename = ''

        try:
            img_id = str(object_id)

            original_img_file = form.cleaned_data.get('image')
            cropping_details = request.POST.get("cropping_details")
            name_bn = form.cleaned_data.get("name_bn")
            name_en = form.cleaned_data.get("name_en")
            img_filename = img_id + '_' + form_name + "_img.jpg"
            information_flag = False
            disease_problem_flag = False

            if form_name == 'subcategory':
                id_list = request.POST.getlist('id[]')
                name_bn_list = request.POST.getlist('name_bn[]')
                details_bn_list = request.POST.getlist('details_bn[]')
                name_en_list = request.POST.getlist('name_en[]')
                details_en_list = request.POST.getlist('details_en[]')

                if is_valid_list(name_bn_list) and is_valid_list(details_bn_list) and is_valid_list(name_en_list) and is_valid_list(details_en_list) and len(name_bn_list) == len(details_bn_list) == len(name_en_list) == len(
                        details_en_list) and all(name_bn_list[i] != name_en_list[i] for i in range(len(name_bn_list))):
                    updated_count = 0
                    created_count = 0

                    if is_valid_list(id_list) and len(id_list) == len(name_bn_list):
                        data = zip(id_list, name_bn_list, details_bn_list, name_en_list, details_en_list)
                        for info_id, info_name_bn, info_details_bn, info_name_en, info_details_en in data:
                            information = Information.objects.get(id=int(info_id), subcategory_id=object_id)

                            if information.name_bn != info_name_bn or information.details_bn != info_details_bn or information.name_en != info_name_en or information.details_en != info_details_en:
                                information.name_bn = info_name_bn
                                information.details_bn = info_details_bn
                                information.name_en = info_name_en
                                information.details_en = info_details_en
                                information.save()
                                updated_count += 1
                    elif len(id_list) < len(name_bn_list):
                        for i in range(len(id_list)):
                            information = Information.objects.get(id=int(id_list[i]), subcategory_id=object_id)

                            if information.name_bn != name_bn_list[i] or information.details_bn != details_bn_list[i] or information.name_en != name_en_list[i] or information.details_en != details_en_list[i]:
                                information.name_bn = name_bn_list[i]
                                information.details_bn = details_bn_list[i]
                                information.name_en = name_en_list[i]
                                information.details_en = details_en_list[i]
                                information.save()
                                updated_count += 1

                        for i in range(len(id_list), len(name_bn_list)):
                            information = Information.objects.create(subcategory_id=object_id, name_bn=name_bn_list[i], details_bn=details_bn_list[i], name_en=name_en_list[i], details_en=details_en_list[i])
                            created_count += 1

                    info_message = ''
                    if updated_count > 1 or created_count > 1:
                        info_message = 'Information'
                    else:
                        info_message = "The information"

                    if updated_count > 0 and created_count > 0:
                        messages.success(request, info_message + " of the " + form_name + " has been added and updated successfully")
                        information_flag = True
                    elif updated_count > 0:
                        messages.success(request, info_message + " of the " + form_name + " has been updated successfully")
                        information_flag = True
                    elif created_count > 0:
                        messages.success(request, info_message + " of the " + form_name + " has been added successfully")
                        information_flag = True
                else:
                    messages.error(request, "Invalid information input, failed to update the information of the " + form_name)
            elif form_name == 'disease_problem':
                insects_causes_bn = form.cleaned_data.get("insects_causes_bn")
                solution_bn = form.cleaned_data.get("solution_bn")
                warning_bn = form.cleaned_data.get("warning_bn")
                insects_causes_en = form.cleaned_data.get("insects_causes_en")
                warning_en = form.cleaned_data.get("warning_en")
                solution_en = form.cleaned_data.get("solution_en")
                if name_bn != name_en and (old_object.insects_causes_bn != insects_causes_bn or old_object.solution_bn != solution_bn or old_object.warning_bn != warning_bn or old_object.insects_causes_en != insects_causes_en or old_object.warning_en != warning_en or old_object.solution_en != solution_en):
                    disease_problem_flag = True

            if original_img_file and cropping_details:
                img_dir_filepath = os.path.join(settings.MEDIA_ROOT, form_name + "_img")
                old_img_filename = img_id + '_' + form_name + "_img_old.jpg"
                temp_img_filename = "temp_" + form_name + "_img" + "." + original_img_file.name.split('.')[-1]

                valid = cropping_image(cropping_details, img_dir_filepath, img_filename, temp_img_filename, old_img_filename)

                if valid:
                    instance.image = form_name + "_img/" + img_filename
                    instance.save()
                    messages.success(request, "The " + form_name.replace('_', '/') + " has been updated successfully")
                else:
                    rollback_update(instance, old_object, form_name, img_dir_filepath, img_filename, temp_img_filename, old_img_filename)
                    messages.error(request, "Invalid image, failed to update the " + form_name.replace('_', '/'))
            elif old_object.name_bn == name_bn and old_object.name_en == name_en and not information_flag and form_name != 'disease_problem':
                messages.error(request, "Invalid input, failed to update the " + form_name.replace('_', '/'))
            elif form_name == 'disease_problem' and not disease_problem_flag:
                rollback_update(instance, old_object, form_name, img_dir_filepath, img_filename, temp_img_filename, old_img_filename)
                messages.error(request, "Invalid input, failed to update the " + form_name.replace('_', '/'))
            elif not original_img_file or not cropping_details or old_object.name_bn != name_bn or old_object.name_en != name_en:
                messages.success(request, "The " + form_name.replace('_', '/') + " has been updated successfully")
            else:
                rollback_update(instance, old_object, form_name, img_dir_filepath, img_filename, temp_img_filename, old_img_filename)
                messages.error(request, "Invalid request, failed to update the " + form_name.replace('_', '/'))

            return redirect(reverse("update-" + form_name.replace('_', '-') + "-form", kwargs={form_name + "_id": object_id}))

        except Exception as e:
            rollback_update(instance, old_object, form_name, img_dir_filepath, img_filename, temp_img_filename, old_img_filename)
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

    else:
        context['form'] = form

    messages.error(request, "Invalid request, failed to updated the " + form_name.replace('_', '/'))
    if form_name == 'category':
        return updateCategoryPage(request, object_id, context)
    elif form_name == 'subcategory':
        return updateSubcategoryPage(request, object_id, context)
    elif form_name == 'disease_problem':
        return update_disease_problem_page(request, object_id, context)
    else:
        messages.error(request, "Invalid " + form_name.replace('_', '/') + " form, try again")
        return viewCategoryPage(request)


def delete_form(request, object_id, data_id=None):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "You are not allow to visit the page")
        return redirect(reverse('index'))

    form_name = 'object'

    if request.POST and user.is_authenticated:
        try:
            parent_url = request.META.get("HTTP_REFERER")
            form_name = parent_url.split("/")[-2].split("-")[1]
            if form_name == 'category':
                category = Category.objects.get(pk=object_id)
                category.delete()
                messages.success(request, "The " + form_name + " has been deleted successfully")
                return redirect(reverse("view-" + form_name))
            elif form_name == 'subcategory':
                if data_id:
                    information = Information.objects.get(id=data_id, subcategory_id=object_id)
                    information.delete()
                    messages.success(request, "The information of the " + form_name + " has been deleted successfully")
                    return redirect(reverse("update-" + form_name + "-form", kwargs={form_name + "_id": object_id}))
                else:
                    subcategory = Subcategory.objects.get(pk=object_id)
                    category_id = subcategory.category.id
                    subcategory.delete()
                    messages.success(request, "The " + form_name + " has been deleted successfully")
                    return redirect(reverse("view-" + form_name, kwargs={"category_id": category_id}))
            elif form_name == 'disease' and data_id:
                disease_problem = DiseaseProblem.objects.get(id=data_id, subcategory_id=object_id)
                disease_problem.delete()
                messages.success(request, "The disease/problem has been deleted successfully")
                return redirect(reverse("view-disease-problem", kwargs={"subcategory_id": object_id}))
        except Exception as e:
            if data_id:
                messages.error(request, "Invalid " + form_name + ", failed to delete the information of the " + form_name)
            else:
                messages.error(request, "Invalid " + form_name + ", failed to delete the " + form_name)
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

    messages.error(request, "Invalid request, failed to delete the " + form_name)
    if form_name in ['category', 'subcategory']:
        return redirect(reverse("view-" + form_name))
    else:
        messages.error(request, "Invalid " + form_name + " form, try again")
        return viewCategoryPage(request)


def get_categories():
    categories = Category.objects.all()
    categories_count = categories.count()
    return {'categories': categories, "categories_count": categories_count}


def get_categories_subcategories():
    categories_subcategories = Category.objects.prefetch_related('subcategories')
    subcategories_count = 0
    if categories_subcategories:
        for category in categories_subcategories:
            subcategories_count += category.subcategories.count()

    return {'categories_subcategories': categories_subcategories, "subcategories_count": subcategories_count}


def get_subcategories_information(category):
    subcategories_information = category.subcategories.prefetch_related('information')
    subcategories_count = subcategories_information.count()
    return {'subcategories_information': subcategories_information, "subcategories_count": subcategories_count}


def get_diseases_problems(subcategory):
    diseases_problems = subcategory.disease_problem.all()
    diseases_problems_count = diseases_problems.count()
    return {'diseases_problems': diseases_problems, "diseases_problems_count": diseases_problems_count}


# Category functions
def viewCategoryPage(request):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}
    user = request.user
    if user.is_authenticated:
        context.update(get_categories())
        return render(request, "managements/view-category.html", context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def insertCategoryPage(request, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language
    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            form = CategoryForm(request.POST, request.FILES)
            return save_form(request, form, context, 'category')
        else:
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, "managements/insert-category.html", context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def updateCategoryPage(request, category_id, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language
    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            return update_form(request, context, 'category', category_id)
        else:
            category = Category.objects.get(pk=category_id)
            context['category'] = category
            subcategories = category.subcategories.all()
            subcategories_count = subcategories.count()
            context["subcategories_count"] = subcategories_count
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, "managements/update-category.html", context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


# Subcategory functions
def viewSubcategoryPage(request, category_id=None):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}
    user = request.user
    if user.is_authenticated:
        try:
            if request.method == 'GET' and category_id is not None:
                category = Category.objects.get(pk=category_id)
                context.update(get_subcategories_information(category))
                context["is_selected"] = True
                context["selected_category"] = category
            else:
                context["is_selected"] = False

            context.update(get_categories())
            context["html_content"] = "<div class=\"col prof-col pt-3\"><h6 class=\"dash-data-col\">No subcategory found!</h6></div>"
            return render(request, 'managements/view-subcategory.html', context)
        except Exception as e:
            messages.error(request, "Invalid category, failed to load the subcategory")
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

        return redirect(reverse("view-subcategory"))

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def insertSubcategoryPage(request, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language
    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            form = SubcategoryForm(request.POST, request.FILES)
            return save_form(request, form, context, 'subcategory')
        else:
            context.update(get_categories())
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'managements/insert-subcategory.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def updateSubcategoryPage(request, subcategory_id, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language
    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            return update_form(request, context, 'subcategory', subcategory_id)
        else:
            context.update(get_categories())
            subcategory = Subcategory.objects.get(id=subcategory_id)
            information = Information.objects.filter(subcategory_id=subcategory_id)
            information_count = information.count()
            context['subcategory'] = subcategory
            context['information'] = information
            context['information_count'] = information_count
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'managements/update-subcategory.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


# Disease/Problem functions
def view_disease_problem_page(request, subcategory_id=None):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}
    user = request.user
    if user.is_authenticated:
        try:
            if request.method == 'GET' and subcategory_id is not None:
                subcategory = Subcategory.objects.get(pk=subcategory_id)
                context.update(get_diseases_problems(subcategory))
                context["is_selected"] = True
                context["selected_subcategory"] = subcategory
            else:
                context["is_selected"] = False

            context.update(get_categories_subcategories())
            context["html_content"] = "<div class=\"col prof-col pt-3\"><h6 class=\"dash-data-col\">No disease/problem found!</h6></div>"
            return render(request, 'managements/view-disease-problem.html', context)
        except Exception as e:
            messages.error(request, "Invalid subcategory, failed to load the disease/problem")
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

        return redirect(reverse("view-disease-problem"))

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def insert_disease_problem_page(request, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language
    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            form = DiseaseProblemForm(request.POST, request.FILES)
            return save_form(request, form, context, 'disease_problem')
        else:
            context.update(get_categories_subcategories())
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'managements/insert-disease-problem.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def update_disease_problem_page(request, disease_problem_id, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language
    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            return update_form(request, context, 'disease_problem', disease_problem_id)
        else:
            context.update(get_categories_subcategories())
            disease_problem = DiseaseProblem.objects.get(pk=disease_problem_id)
            context['disease_problem'] = disease_problem
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'managements/update-disease-problem.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


# Extra
def accounts_page(request, account_id=None, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.method == "GET" and account_id and len(context) == 1:
            account = Account.objects.get(id=account_id)
            filters = request.GET.get('action')
            if filters:
                if filters == "Demote-staff" and account.is_staff:
                    account.is_staff = False
                    account.save()
                    create_notification(request, user, account_id, "You have been demoted from staff")
                    messages.success(request, "The account has been demoted from staff successfully")
                elif filters == "Promote-staff" and not account.is_staff:
                    account.is_staff = True
                    account.save()
                    create_notification(request, user, account_id, "You have been promoted to staff")
                    messages.success(request, "The account has been promoted to staff successfully")
                elif filters == "Demote-expert" and account.expert:
                    account.expert = False
                    account.save()
                    create_notification(request, user, account_id, "You have been demoted from expert")
                    messages.success(request, "The account has been demoted from expert successfully")
                elif filters == "Promote-expert" and not account.expert:
                    account.expert = True
                    account.save()
                    create_notification(request, user, account_id, "You have been promoted to expert")
                    messages.success(request, "The account has been promoted to expert successfully")
                elif filters == "Delete":
                    account.delete()
                    messages.success(request, "The account has been deleted successfully")
                else:
                    messages.error(request, "Invalid action request, failed to take action to the account")

                return redirect(reverse("accounts"))
        else:
            accounts = Account.objects.all()
            context["accounts"] = accounts
            context["accounts_count"] = accounts.count()
            return render(request, 'managements/accounts.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def expert_requests_page(request, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            form = RoomForm(request.POST)
            if form.is_valid():
                instance = form.save()
                create_notification(request, user, instance.user.id, "The expert request has been approved successfully")
                messages.success(request, "The room has been created successfully")
                return redirect(reverse('expert-requests'))
            else:
                context['form'] = form

            messages.error(request, "Invalid room request, failed to create the room")
            return expert_requests_page(request, context)
        else:
            accounts = Account.objects.all()
            accounts = [account for account in accounts if account.expert]
            problems = Problem.objects.all()
            rooms = Room.objects.all()
            context["accounts"] = accounts
            context["problems"] = problems
            context["problems_count"] = problems.count()
            context["rooms"] = rooms
            context["rooms_count"] = rooms.count()
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'managements/expert-requests.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def delete_room(request, room_id):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}

    user = request.user
    if user.is_authenticated:
        if request.method == "GET":
            room = Room.objects.get(id=room_id)
            room.delete()
            messages.success(request, "The room has been deleted successfully")
            return redirect(reverse('expert-requests'))
        else:
            messages.error(request, "Invalid request, failed to delete the room")

        return redirect(reverse('expert-requests'))

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def delete_problem(request, problem_id):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}

    user = request.user
    if user.is_authenticated:
        if request.POST:
            problem = Problem.objects.get(id=problem_id)
            problem.delete()
            messages.success(request, "The problem has been deleted successfully")
            return redirect(reverse('expert-requests'))
        else:
            messages.error(request, "Invalid request, failed to delete the problem")

        return redirect(reverse('expert-requests'))

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))
