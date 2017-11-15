# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json

from django.shortcuts import render
from decouple import config
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError

EDAMAM_ACCESS_KEY = config('EDAMAM_ACCESS_KEY')
EDAMAM_APP_ID = config('EDAMAM_APP_ID')

# Create your views here.
def call_recipe_search(search_term):
    recipe_search_url = 'https://api.edamam.com/search'
    payload = {
        'app_id' : EDAMAM_APP_ID,
        'app_key' : EDAMAM_ACCESS_KEY,
        'q' : search_term,
        'to' : 999,
    }
    r = requests.get(recipe_search_url, params=payload)
    results = json.loads(r.text)
    return results
    
def home(request):
    if request.method == "GET":
        try:
            search_term = request.GET['search_term']
            results = call_recipe_search(search_term)
            recipe_list = results['hits']
        except MultiValueDictKeyError:
            recipe_list= []
            search_term = None
    elif request.method == "POST":
        search_term = request.POST.get('search_term')
        results = call_recipe_search(search_term)
        recipe_list = results['hits']
    else:
        recipe_list= []
        search_term = None
    
    paginator = Paginator(recipe_list, 5, allow_empty_first_page=True) # Show 5 recipes per page
    page = request.GET.get('page')
    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recipes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recipes = paginator.page(paginator.num_pages)
    
    context = {
        'recipes' : recipes,
        'search_term': search_term
    }
    
    return render(request, 'search/home.html', context)