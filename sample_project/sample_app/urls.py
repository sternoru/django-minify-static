from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'sample_app.views.index')
)