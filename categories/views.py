from django.shortcuts import render
from django.views.generic import ListView

from categories.models import Category


# Create your views here.


class ListCategories(ListView[Category]):
    # template name default will be category_list.html
    model = Category
    context_object_name = "categories"
