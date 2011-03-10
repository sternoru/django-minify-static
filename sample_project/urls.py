from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^minify/', include('minify.urls')),
    (r'^', include('sample_app.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
