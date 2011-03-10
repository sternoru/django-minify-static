"""
Url configuration pointing to views handling minifiying
"""

from django.conf.urls.defaults import *

from minify import views

urlpatterns = patterns('',    
    url(r'^js/$', views.js_minify, name='minify_js'),
    url(r'^css/$', views.css_minify, name='minify_css'),
    url(r'^js2/$', views.js_nominify, name='nominify_js'),
    url(r'^css2/$', views.css_nominify, name='nominify_css'),
)