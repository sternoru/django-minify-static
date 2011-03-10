# Create your views here.

from django import http, shortcuts

def index(request):
    return shortcuts.render_to_response('index.html')