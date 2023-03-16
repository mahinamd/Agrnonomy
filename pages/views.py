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


def categoryPage(request):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}

    title = get_category_title()
    context['categories_title'] = title
    categories = get_category()
    context['categories'] = categories

    user = request.user
    if user.is_authenticated:
        return render(request, 'category.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect('index')


def subcategoryPage(request, index):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}

    found = find_category_index(index)

    if found == -1:
        messages.error(request, "Invalid subcategory!")
        return redirect('category')

    context['parent'] = found[1]
    title = get_subcategory_title()
    context['subcategories_title'] = title
    subcategories = get_subcategory(found[0])
    context['subcategories'] = subcategories

    user = request.user
    if user.is_authenticated:
        return render(request, 'subcategory.html', context)

    messages.error(request, "You are not allow to visit the page")
    return redirect('index')


class Counter(object):
    def __init__(self):
        self.c = 0

    def increase(self):
        self.c += 1
        return ''

    def value(self):
        return self.c


def informationPage(request, parent, index):
    default_language = 'bn' in translation.get_language()
    context = {'default_language': default_language}

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
