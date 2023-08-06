import os
import traceback

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.contrib import messages
from Agronomy.connection import get_collection

from accounts.models import Account
from accounts.views import create_notification
from managements.models import Category, Subcategory, Information, DiseaseProblem
from managements.views import cropping_image, get_categories, get_categories_subcategories, get_subcategories_information, get_diseases_problems

from .models import Question, QuestionCounts, Answer, AnswerCounts, Vote, Problem, Room, Message
from .forms import QuestionForm, AnswerForm, ProblemForm
from django.db import models
import copy


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


def get_category_title():
    collection = get_collection(1)
    data = collection.find({}, {'_id': 0, 'title': 1})
    title = ""

    for result in data:
        title = result['title'][0]['category_title']
        break

    return title


def get_category():
    collection = get_collection(1)
    data = collection.find({}, {'_id': 0, 'title': 1, 'categories_image': 1})
    categories_title = []
    index_categories = []
    categories_image = []
    for result in data:
        categories_title = [result['title'][0]['categories']['0'],
                            result['title'][0]['categories']['1'],
                            result['title'][0]['categories']['2'],
                            result['title'][0]['categories']['3'],
                            result['title'][0]['categories']['4'],
                            result['title'][0]['categories']['5']]
        index_categories = [result['title'][0]['index_categories']['0'],
                            result['title'][0]['index_categories']['1'],
                            result['title'][0]['index_categories']['2'],
                            result['title'][0]['index_categories']['3'],
                            result['title'][0]['index_categories']['4'],
                            result['title'][0]['index_categories']['5']]
        categories_image = [result['categories_image']['0'],
                            result['categories_image']['1'],
                            result['categories_image']['2'],
                            result['categories_image']['3'],
                            result['categories_image']['4'],
                            result['categories_image']['5']]
        break

    categories = zip(categories_title, index_categories, categories_image)

    return categories


def get_subcategory_title():
    collection = get_collection(1)
    data = collection.find({}, {'_id': 0, 'title': 1})
    title = ""

    for result in data:
        title = result['title'][0]['subcategory_title']
        break

    return title


def get_information_title():
    collection = get_collection(2)
    data = collection.find({}, {'_id': 0, 'data': 1})
    title = ""

    for result in data:
        title = result['data'][0]['information_title']
        break

    return title


def find_category_index(index):
    collection = get_collection(1)
    data = collection.find({}, {'_id': 0, 'title.index_categories': 1})
    dic = {}

    for result in data:
        dic.update(result['title'][0]['index_categories'])

    for key, value in dic.items():
        if value == index:
            return [int(key), value]

    return -1


def find_subcategory_index(parent_index, index):
    collection = get_collection(1)
    data = collection.find({}, {'_id': 0, 'title.index_subcategories': 1})
    dic = {}

    for result in data:
        dic.update(result['title'][0]['index_subcategories'][parent_index])

    for key, value in dic.items():
        if value == index:
            return [int(key), value]

    return -1


def get_subcategory(index):
    collection = get_collection(1)
    data1 = collection.find({}, {'_id': 0, 'title.subcategories': 1})
    data2 = collection.find({}, {'_id': 0, 'title.index_subcategories': 1})
    data3 = collection.find({}, {'_id': 0, 'title.subcategories_image': 1})
    subcategories_title = []
    index_subcategories = []
    subcategories_image = []
    dic = {}

    for result in data1:
        dic.update(result['title'][0]['subcategories'][index])

    for key, value in dic.items():
        subcategories_title.append(value)

    subcategories_title.pop(0)
    dic = {}

    for result in data2:
        dic.update(result['title'][0]['index_subcategories'][index])

    for key, value in dic.items():
        index_subcategories.append(value)

    index_subcategories.pop(0)
    dic = {}

    for result in data3:
        dic.update(result['title'][0]['subcategories_image'][index])

    for key, value in dic.items():
        subcategories_image.append(value)

    subcategories_image.pop(0)
    subcategories = zip(subcategories_title, index_subcategories, subcategories_image)

    return subcategories


def get_information(parent_index, index):
    collection = get_collection(2)
    collection_name = "information_" + str(parent_index)
    data1 = collection.find({}, {'_id': 0, 'data.information_column': 1})
    data2 = collection.find({}, {'_id': 0, 'data.' + collection_name: 1})
    data3 = collection.find({}, {'_id': 0, 'data.' + collection_name: 1})

    column = []
    row = []
    image = []
    warning = []
    solutions = []
    causes = []
    disease = []
    found_image = False
    dic = {}

    for result in data1:
        dic.update(result['data'][0]['information_column'][parent_index])

    for key, value in dic.items():
        column.append(value)

    column.pop(0)
    dic = {}

    for result in data2:
        dic.update(result['data'][0][collection_name][index])

    for key, value in dic.items():
        row.append(value)

    row.pop(0)
    dic = {}

    for result in data3:
        if 'information_image' in result['data'][0][collection_name][index]:
            found_image = True
            dic.update(result['data'][0][collection_name][index]['information_image'])

    if found_image:
        for key, value in dic.items():
            image.append(value)

        dic = {}
        dic.update(row[4][0])
        for key, value in dic.items():
            disease.append(value)

        dic = {}
        dic.update(row[5][0])
        for key, value in dic.items():
            causes.append(value)

        dic = {}
        dic.update(row[6][0])
        for key, value in dic.items():
            solutions.append(value)

        dic = {}
        dic.update(row[7][0])
        for key, value in dic.items():
            warning.append(value)

        try:
            disease.remove('')
            causes.remove('')
            solutions.remove('')
            warning.remove('')
            image.remove('')
        except ValueError:
            pass

        return [found_image, column[4], column[5], column[6], column[7], zip(causes, image),
                zip(disease, solutions, warning), zip(column, row)]
    else:
        return [found_image, zip(column, row)]


def get_subcategory_info(parent_index, index):
    collection = get_collection(1)
    data1 = collection.find({}, {'_id': 0, 'title.subcategories': 1})
    data2 = collection.find({}, {'_id': 0, 'title.subcategories_image': 1})
    title = ""
    image = ""

    for result in data1:
        title = result['title'][0]['subcategories'][parent_index][str(index)]

    for result in data2:
        image = result['title'][0]['subcategories_image'][parent_index][str(index)]

    return [title, image]


def category_page(request):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}

    '''
    title = get_category_title()
    context['categories_title'] = title
    categories = get_category()
    context['categories'] = categories
    '''

    user = request.user
    if user.is_authenticated:
        context.update(get_categories())
        return render(request, "category.html", context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def subcategory_page(request, category_id):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}

    '''
    found = find_category_index(index)

    if found == -1:
        messages.error(request, "Invalid subcategory!")
        return redirect('category')

    context['parent'] = found[1]
    title = get_subcategory_title()
    context['subcategories_title'] = title
    subcategories = get_subcategory(found[0])
    context['subcategories'] = subcategories
    '''

    user = request.user
    if user.is_authenticated:
        try:
            category = Category.objects.get(id=category_id)
            context.update(get_subcategories_information(category))
            context["category"] = category
            return render(request, 'subcategory.html', context)
        except Exception as e:
            messages.error(request, "Invalid category, failed to load the subcategory")
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

        return redirect(reverse("category"))

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


class Counter(object):
    def __init__(self):
        self.c = 0

    def increase(self):
        self.c += 1
        return ''

    def value(self):
        return self.c


def information_page(request, category_id, subcategory_id):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}

    user = request.user
    if user.is_authenticated:
        try:
            category = Category.objects.get(id=category_id)
            subcategory = Subcategory.objects.get(id=subcategory_id)
            context.update(get_diseases_problems(subcategory))
            context["category"] = category
            context["subcategory"] = subcategory
            return render(request, 'information.html', context)
        except Exception as e:
            messages.error(request, "Invalid category, failed to load the subcategory")
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

        return redirect(reverse("subcategory", kwargs={"category_id": category_id}))

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def informationPage(request, parent, index):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}

    found_parent = find_category_index(parent)
    found_index = find_subcategory_index(found_parent[0], index)

    if found_parent == -1 or found_index == -1:
        messages.error(request, "Invalid information!")
        return redirect('category')

    title = get_information_title()
    context['information_title'] = title
    context['parent'] = found_parent[1]
    parent_info = get_subcategory_info(found_parent[0], found_index[0])
    context['parent_title'] = parent_info[0]
    context['parent_url'] = parent_info[1]
    info = get_information(found_parent[0], found_index[0])
    context['has_image'] = info[0]
    if context['has_image']:
        context['disease_header'] = info[1]
        context['cause_header'] = info[2]
        context['solution_header'] = info[3]
        context['warning_header'] = info[4]
        context['causes'] = info[5]
        context['definition'] = info[6]
        context['information'] = info[7]
    else:
        context['information'] = info[1]

    context['counter'] = Counter()

    user = request.user
    if user.is_authenticated:
        return render(request, 'information.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect('index')


# Supporting functions
def save_form(request, form, context, form_name, question=None):
    if form.is_valid():
        instance = form.save(commit=False)
        instance.account = request.user
        if form_name == 'answer':
            if question:
                instance.question = question
            else:
                messages.error(request, "Invalid request for question, failed to post the " + form_name.replace('_', '/'))

        instance.save()
        img_dir_filepath = ''
        temp_img_filename = ''
        img_filename = ''

        try:
            img_id = str(instance.id)

            original_img_file = form.cleaned_data.get('image')
            cropping_details = request.POST.get("cropping_details")

            if form_name == 'question':
                tags = form.cleaned_data.get("tags")
                if tags:
                    split_list = tags.split(',')
                    cleaned_list = [' '.join(item.strip().split()) for item in split_list if item != '']
                    tags_list = ['#' + item for item in cleaned_list]
                    tags = ", ".join(tags_list)
                    instance.tags = tags
                    instance.save()

            if original_img_file and "default/" not in str(original_img_file) and cropping_details:
                img_dir_filepath = os.path.join(settings.MEDIA_ROOT, form_name + "_img")
                img_filename = img_id + '_' + form_name + "_img.jpg"
                temp_img_filename = "temp_" + form_name + "_img" + '.' + original_img_file.name.split('.')[-1]

                valid = cropping_image(cropping_details, img_dir_filepath, img_filename, temp_img_filename)

                if valid:
                    instance.image = form_name + "_img/" + img_filename
                    instance.save()
                    messages.success(request, "The " + form_name.replace('_', '/') + " has been posted successfully")
                else:
                    # rollback_save(instance, img_dir_filepath, img_filename, temp_img_filename)
                    messages.error(request, "Invalid image, failed to post the " + form_name.replace('_', '/'))
            elif "default/" in str(original_img_file):
                messages.success(request, "The " + form_name.replace('_', '/') + " has been posted successfully")
            else:
                # rollback_save(instance, img_dir_filepath, img_filename, temp_img_filename)
                messages.error(request, "Invalid request, failed to post the " + form_name.replace('_', '/'))

            if form_name == 'question':
                return redirect(reverse("questions", kwargs={"question_id": instance.id}))
            elif question and form_name == 'answer':
                return redirect(reverse("questions", kwargs={"question_id": question.id}))

        except Exception as e:
            # rollback_save(instance, img_dir_filepath, img_filename, temp_img_filename)
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()
    else:
        context['form'] = form

    messages.error(request, "Invalid request, failed to post the " + form_name.replace('_', '/'))
    if form_name == 'question':
        return ask_question_page(request, context)
    elif question and form_name == 'answer':
        return view_question_page(request, question.id, context)
    else:
        messages.error(request, "Invalid " + form_name.replace('_', '/') + " form, try again")
        return questions_page(request)


# Question functions
def questions_page(request):
    default_language = 'bn' in translation.get_language()
    context = {"default_language": default_language}

    user = request.user
    if user.is_authenticated:
        try:
            filters = request.GET.get('tab')
            if filters:
                filters = filters.split(',') if ',' in filters else filters
                if isinstance(filters, list) and len(filters) == 2 and "Newest" in filters and "Unanswered" in filters:
                    questions = Question.objects.filter(answers__isnull=True).order_by('-created')
                elif filters == "Newest":
                    questions = Question.objects.order_by('-created')
                elif filters == "Unanswered":
                    questions = Question.objects.filter(answers__isnull=True)
                else:
                    messages.error(request, "Invalid tab request, failed to load the questions")
                    return redirect(reverse("questions"))
            else:
                questions = Question.objects.all()

            context["questions"] = questions
            context["questions_count"] = questions.count()
            return render(request, 'questions.html', context)
        except Exception as e:
            messages.error(request, "Invalid request, failed to load questions")
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

        return redirect(reverse("questions"))

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def ask_question_page(request, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            form = QuestionForm(request.POST, request.FILES)
            return save_form(request, form, context, 'question')
        else:
            url_parse = urlparse(request.META.get("HTTP_REFERER"))
            question_id = None
            if url_parse.path:
                resolve_kwargs = resolve(url_parse.path).kwargs
                if resolve_kwargs:
                    for key, value in resolve_kwargs.items():
                        if key == "question_id":
                            question_id = value

            context["question_id"] = question_id
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'ask-question.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def view_question_page(request, question_id, answer_id=None, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        try:
            if request.POST and len(context) == 1:
                form = AnswerForm(request.POST, request.FILES)
                question = Question.objects.get(id=question_id)
                return save_form(request, form, context, 'answer', question)
            else:
                print(question_id)
                question = Question.objects.get(id=question_id)
                question.question_counts.views_count += 1
                question.question_counts.save()

                filters = request.GET.get('tab')
                if filters:
                    filters = filters.split(',') if ',' in filters else filters
                    if isinstance(filters, list) and len(filters) == 2 and "Newest" in filters and "Highest-vote" in filters:
                        answers = question.answers.order_by('-answer_counts__votes_count', '-created')
                    elif filters == "Newest":
                        answers = question.answers.order_by('-created')
                    elif filters == "Highest-vote":
                        answers = question.answers.order_by('-answer_counts__votes_count')
                    else:
                        messages.error(request, "Invalid tab request, failed to load answers of the question")
                        return redirect(reverse("questions", kwargs={"question_id": question_id}))
                else:
                    answers = question.answers.all()

                user_has_answered = any(answer.account == user for answer in answers)

                filters = request.GET.get('vote')
                if filters:
                    if question.account_id != user.id and not answer_id:
                        account_ids = question.question_counts.voted_by.values_list('id', flat=True)
                        user_exists = user.id in account_ids
                        if filters == "Up":
                            if not user_exists:
                                question.question_counts.votes_count += 1
                                question.question_counts.save()
                                Vote.objects.create(account=user, question_vote=question.question_counts, upvote=True)
                            else:
                                vote = Vote.objects.get(account=user, question_vote=question.question_counts)
                                if not vote.upvote:
                                    question.question_counts.votes_count += 1
                                    question.question_counts.save()
                                    vote.delete()
                                else:
                                    messages.error(request, "Invalid up vote request, failed to up vote for the question")
                        elif filters == "Down":
                            if not user_exists:
                                question.question_counts.votes_count -= 1
                                question.question_counts.save()
                                Vote.objects.create(account=user, question_vote=question.question_counts)
                            else:
                                vote = Vote.objects.get(account=user, question_vote=question.question_counts)
                                if vote.upvote:
                                    question.question_counts.votes_count -= 1
                                    question.question_counts.save()
                                    vote.delete()
                                else:
                                    messages.error(request, "Invalid down vote request, failed to down vote for the question")
                        else:
                            messages.error(request, "Invalid vote request, failed to vote for the question")
                    elif answer_id:
                        answer = Answer.objects.get(id=answer_id)
                        if answer.account_id != user.id:
                            user_exists = False
                            for temp_answer in answers:
                                account_ids = temp_answer.answer_counts.voted_by.values_list('id', flat=True)
                                if user.id in account_ids:
                                    user_exists = True
                                    break

                            if filters == "Up":
                                account_ids = answer.answer_counts.voted_by.values_list('id', flat=True)
                                if not user_exists:
                                    answer.answer_counts.votes_count += 1
                                    answer.answer_counts.save()
                                    Vote.objects.create(account=user, answer_vote=answer.answer_counts, upvote=True)
                                elif user.id in account_ids:
                                    vote = Vote.objects.get(account=user, answer_vote=answer.answer_counts)
                                    if not vote.upvote:
                                        answer.answer_counts.votes_count += 1
                                        answer.answer_counts.save()
                                        vote.delete()
                                    else:
                                        messages.error(request, "Invalid up vote request, you already up vote the answer")
                                else:
                                    messages.error(request, "Invalid up vote request, failed to up vote for the answer")
                            elif filters == "Down":
                                account_ids = answer.answer_counts.voted_by.values_list('id', flat=True)
                                if not user_exists:
                                    answer.answer_counts.votes_count -= 1
                                    answer.answer_counts.save()
                                    Vote.objects.create(account=user, answer_vote=answer.answer_counts)
                                elif user.id in account_ids:
                                    vote = Vote.objects.get(account=user, answer_vote=answer.answer_counts)
                                    if vote.upvote:
                                        answer.answer_counts.votes_count -= 1
                                        answer.answer_counts.save()
                                        vote.delete()
                                    else:
                                        messages.error(request, "Invalid down vote request, you already down vote the answer")
                                else:
                                    messages.error(request, "Invalid down vote request, failed to down vote for the answer")
                            else:
                                messages.error(request, "Invalid vote request, failed to vote for the answer")
                        else:
                            messages.error(request, "Invalid vote request, you are not allowed to vote for the answer")
                    else:
                        messages.error(request, "Invalid vote request, you are not allowed to vote")

                    return redirect(reverse("questions", kwargs={"question_id": question_id}))

                filters = request.GET.get('accept')
                if filters:
                    if question.account_id == user.id and answer_id:
                        answer = question.answers.get(id=answer_id)
                        if filters == "Yes" and answer and not answer.is_accepted and not question.has_accepted_answer:
                            answer.is_accepted = True
                            answer.save()
                        elif filters == "No" and answer and answer.is_accepted and question.has_accepted_answer:
                            answer.is_accepted = False
                            answer.save()
                        else:
                            messages.error(request, "Invalid accept request, failed to accept the answer")
                    else:
                        messages.error(request, "Invalid accept request, you are not allowed to accept the answer")

                    return redirect(reverse("questions", kwargs={"question_id": question_id}))

                context["question"] = question
                context["answers"] = answers
                context["answers_count"] = answers.count()
                context["user_has_answered"] = user_has_answered
                context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
                return render(request, 'view-question.html', context)
        except Exception as e:
            messages.error(request, "Invalid request, failed to load the question")
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

        return redirect(reverse("questions"))

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def update_form(request, context, form_name, object_id, parent_id=None):
    update_object = None
    form = None
    if form_name == 'question':
        update_object = Question.objects.get(pk=object_id)
        form = QuestionForm(request.POST, request.FILES, instance=update_object)
    elif form_name == 'answer':
        update_object = Answer.objects.get(pk=object_id)
        form = AnswerForm(request.POST, request.FILES, instance=update_object)

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
            title = tags = ''
            if form_name == 'question':
                title = form.cleaned_data.get("title")

            if form_name == 'question':
                tags = form.cleaned_data.get("tags")
                if tags and old_object.tags != tags:
                    split_list = tags.split(',')
                    cleaned_list = [' '.join(item.strip().split()) for item in split_list if item != '']
                    tags_list = ['#' + item for item in cleaned_list]
                    tags = ", ".join(tags_list)
                    instance.tags = tags
                    instance.save()

            description = form.cleaned_data.get("description")
            img_filename = img_id + '_' + form_name + "_img.jpg"

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
                    #rollback_update(instance, old_object, form_name, img_dir_filepath, img_filename, temp_img_filename, old_img_filename)
                    messages.error(request, "Invalid image, failed to update the " + form_name.replace('_', '/'))
            elif (form_name == 'question' and old_object.description == description and old_object.title == title and old_object.tags == tags) or (form_name == 'answer' and old_object.description == description):
                messages.error(request, "Invalid input, failed to update the " + form_name.replace('_', '/'))
            elif not original_img_file or not cropping_details or old_object.description != description:
                messages.success(request, "The " + form_name.replace('_', '/') + " has been updated successfully")
            else:
                #rollback_update(instance, old_object, form_name, img_dir_filepath, img_filename, temp_img_filename, old_img_filename)
                messages.error(request, "Invalid request, failed to update the " + form_name.replace('_', '/'))

            if form_name == 'question':
                return redirect(reverse("questions", kwargs={"question_id": object_id}))
            if form_name == 'answer' and parent_id:
                return redirect(reverse("questions", kwargs={"question_id": parent_id}))


        except Exception as e:
            #rollback_update(instance, old_object, form_name, img_dir_filepath, img_filename, temp_img_filename, old_img_filename)
            print("Exception: " + str(e))
            print("Traceback: ")
            traceback.print_exc()

    else:
        context['form'] = form

    messages.error(request, "Invalid request, failed to updated the " + form_name.replace('_', '/'))
    if form_name == 'question':
        return update_question_page(request, object_id, context)
    elif form_name == 'answer' and parent_id:
        return update_answer_page(request, parent_id, object_id, context)
    else:
        messages.error(request, "Invalid " + form_name.replace('_', '/') + " form, try again")
        return questions_page(request)


def update_question_page(request, question_id, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            return update_form(request, context, 'question', question_id)
        else:
            question = Question.objects.get(id=question_id)
            context["question"] = question
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'update-question.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def delete_question_page(request, question_id, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            Question.objects.get(id=question_id).delete()
            messages.success(request, "The question has been deleted successfully")
            return redirect(reverse("questions"))
        else:
            messages.error(request, "Invalid request, failed to delete the question")
            question = Question.objects.get(id=question_id)
            context["question"] = question
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'update-question.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def update_answer_page(request, question_id, answer_id, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            return update_form(request, context, 'answer', answer_id, question_id)
        else:
            question = Question.objects.get(id=question_id)
            answer = Answer.objects.get(id=answer_id)
            context["question"] = question
            context["answer"] = answer
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'update-answer.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def delete_answer_page(request, question_id, answer_id, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            Answer.objects.get(id=answer_id).delete()
            messages.success(request, "The answer has been deleted successfully")
            return redirect(reverse("questions", kwargs={"question_id": question_id}))
        else:
            messages.error(request, "Invalid request, failed to delete the answer")
            question = Question.objects.get(id=question_id)
            answer = Answer.objects.get(id=answer_id)
            context["question"] = question
            context["answer"] = answer
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'update-answer.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def chat_expert_page(request, problem_id=None, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.method == "GET" and len(context) == 1:
            account = Account.objects.get(id=user.id)
            if problem_id:
                case = Problem.objects.get(id=problem_id)
                context["case"] = case

                if case.has_room:
                    if default_language:
                        ws_url = "wss://" + request.get_host() + "/chat/room/" + str(case.room.id)
                    else:
                        ws_url = "wss://" + request.get_host() + "/en/chat/room/" + str(case.room.id)

                    context["ws_url"] = ws_url
                    room = account.user_rooms.get(problem_id=problem_id)
                    room_messages = room.room_messages.all()
                    context["room"] = room
                    context["room_messages"] = room_messages
                    context["room_messages_count"] = room_messages.count()

            problems = account.chat_problems.all()
            problems = [problem for problem in problems if not problem.has_room or (problem.has_room and not problem.room.ai)]
            context["problems"] = problems
            context["problems_count"] = len(problems)
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'chat/chat-expert.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def chat_user_page(request, problem_id=None, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.method == "GET" and len(context) == 1:
            account = Account.objects.get(id=user.id)
            if problem_id:
                case = Problem.objects.get(id=problem_id)
                context["case"] = case
                if default_language:
                    ws_url = "wss://" + request.get_host() + "/chat/room/" + str(case.room.id)
                else:
                    ws_url = "wss://" + request.get_host() + "/en/chat/room/" + str(case.room.id)

                context["ws_url"] = ws_url
                room = account.expert_rooms.get(problem_id=problem_id)

                room_messages = room.room_messages.all()
                context["room"] = room
                context["room_messages"] = room_messages
                context["room_messages_count"] = room_messages.count()

            expert_rooms = account.expert_rooms.all()
            context["expert_rooms"] = expert_rooms
            context["expert_rooms_count"] = expert_rooms.count()
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'chat/chat-user.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def request_expert_page(request, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            form = ProblemForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.account = user
                tags = form.cleaned_data.get("tags")
                if tags:
                    split_list = tags.split(',')
                    cleaned_list = [' '.join(item.strip().split()) for item in split_list if item != '']
                    tags_list = ['#' + item for item in cleaned_list]
                    tags = ", ".join(tags_list)
                    instance.tags = tags

                instance.save()
                messages.success(request, "The expert request has been send successfully")
                return redirect(reverse('chat-expert'))
            else:
                context['form'] = form

            messages.error(request, "Invalid expert request, failed to send the request")
            return request_expert_page(request, context)
        else:
            return render(request, 'chat/request-expert.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def request_ai_page(request, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.POST and len(context) == 1:
            form = ProblemForm(request.POST)
            if form.is_valid():
                problem = form.save(commit=False)
                problem.account = user
                tags = form.cleaned_data.get("tags")
                if tags:
                    split_list = tags.split(',')
                    cleaned_list = [' '.join(item.strip().split()) for item in split_list if item != '']
                    tags_list = ['#' + item for item in cleaned_list]
                    tags = ", ".join(tags_list)
                    problem.tags = tags

                problem.save()
                room = Room.objects.create(problem=problem, user=user, ai=True, assigned=True)
                Message.objects.create(room=room, content="Please describe your problem.")
                create_notification(request, user, user.id, "The AI (ChatGPT) request has been approved successfully")
                messages.success(request, "The AI (ChatGPT) request has been approved successfully")
                return redirect(reverse('chat-ai'))
            else:
                context['form'] = form

            messages.error(request, "Invalid AI request, failed to approve the request")
            return request_expert_page(request, context)
        else:
            return render(request, 'chat/request-ai.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))


def chat_ai_page(request, problem_id=None, context=None):
    if context is None:
        context = {}
    default_language = 'bn' in translation.get_language()
    context["default_language"] = default_language

    user = request.user
    if user.is_authenticated:
        if request.method == "GET" and len(context) == 1:
            account = Account.objects.get(id=user.id)
            if problem_id:
                case = Problem.objects.get(id=problem_id)
                context["case"] = case
                if default_language:
                    ws_url = "wss://" + request.get_host() + "/chat/ai/room/" + str(case.room.id)
                else:
                    ws_url = "wss://" + request.get_host() + "/en/chat/ai/room/" + str(case.room.id)

                context["ws_url"] = ws_url
                room = account.user_rooms.get(problem_id=problem_id)
                room_messages = room.room_messages.all()
                context["room"] = room
                context["room_messages"] = room_messages
                context["room_messages_count"] = room_messages.count()

            problems = account.chat_problems.all()
            problems = [problem for problem in problems if problem.has_room and problem.room.ai]
            context["problems"] = problems
            context["problems_count"] = len(problems)
            context["DATA_UPLOAD_MAX_MEMORY_SIZE"] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
            return render(request, 'chat/chat-ai.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect(reverse('index'))

