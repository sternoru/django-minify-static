"""
Views
"""

import os

from django import http
from django.views.decorators import cache as cache_decorators

from minify import app_settings
from minify import utils

CSS_JS_EXPIRES =  app_settings.MINIFY_CSS_JS_EXPIRES
CACHE_DURATION =  app_settings.MINIFY_CACHE_DURATION
PRIVATE = app_settings.MINIFY_HEADER_CACHE_PRIVATE
MAX_AGE = CSS_JS_EXPIRES * 24 * 60 * 60

@cache_decorators.cache_page(CACHE_DURATION)
@cache_decorators.cache_control(private=PRIVATE, must_revalidate=True, max_age=MAX_AGE, proxy_revalidate=True, s_max_age=MAX_AGE)
def js_minify(request):
    """View to render minified/combined Javascript
    
    Params:
    - request: a django.http.HttpRequest object
    
    Returns:
    - response: a django.http.HttpResponse with combined
    and minified Javascript as its content 
    """
    res = ''    
    files = []
    url = request.GET.get('url')
    if url:
        minified_js = utils.minify_js_from_url(request, url)
        if minified_js:
            res = '%s\n%s' % (res, minified_js)
    if request.GET.get('files'):
        files = request.GET['files'].split(',')
        res = '%s\n%s' % (res, utils.minify_js_from_files(request, files))
    response = http.HttpResponse(res, mimetype='text/javascript')
    return response

@cache_decorators.cache_page(CACHE_DURATION)
@cache_decorators.cache_control(private=PRIVATE, must_revalidate=True, max_age=MAX_AGE, proxy_revalidate=True, s_max_age=MAX_AGE)
def css_minify(request):
    """View to render minified/combined CSS
    
    Params:
    - request: a django.http.HttpRequest object
    
    Returns:
    - response: a django.http.HttpResponse with combined
    and minified CSS as its content 
    """
    res = ''
    files = [] 
    if request.GET.get('files'):
        files = request.GET['files'].split(',')
        res = utils.minify_css_from_files(request, files)
    response = http.HttpResponse(res, mimetype='text/css')
    return response

@cache_decorators.never_cache
def js_nominify(request):
    """View to render not minified/not combined Javascript
    
    Params:
    - request: a django.http.HttpRequest object
    
    Returns:
    - response: a django.http.HttpResponse with not combined
    and not minified Javascript as its content 
    """
    js = ''
    if 'url' in request.GET:
        return utils.minify_js_from_url(request, request.GET['url'], nominify=True)
    if 'file' in request.GET:
        filename = request.GET['file']
        js = utils.check_and_read_from_file(request, filename)
    response = http.HttpResponse(js, mimetype='text/javascript')
    return response 

@cache_decorators.never_cache
def css_nominify(request):
    """View to render not minified/not combined CSS
    
    Params:
    - request: a django.http.HttpRequest object
    
    Returns:
    - response: a django.http.HttpResponse with not combined
    and not minified CSS as its content 
    """
    css = ''
    if 'file' in request.GET:
        filename = request.GET['file']
        css = utils.check_and_read_from_file(request, filename)
    response = http.HttpResponse(css, mimetype='text/css') 
    return response
