from django.http import HttpResponse
from django.shortcuts import render

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context)


def about(request):
    context = {}
    return render(request, 'rango/about.html', context)


def category(request, category_name_slug):
    context = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context['category_name'] = category.name

        pages = Page.objects.filter(category=category)
        context['pages'] = pages
        context['category'] = category
        context['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'Post':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context)
