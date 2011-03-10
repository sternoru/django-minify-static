"""
Tag rendering tags pointing ot minified/not-minified
Javascript or CSS content
"""

from django import template
from django.core import urlresolvers

from minify import app_settings

register = template.Library()


MINIFY_JS_URL = urlresolvers.reverse('minify_js')
MINIFY_CSS_URL = urlresolvers.reverse('minify_css')
NOMINIFY_JS_URL = urlresolvers.reverse('nominify_js')
NOMINIFY_CSS_URL = urlresolvers.reverse('nominify_css')


@register.inclusion_tag('minify/js.html')
def js(files_in_string, from_url=None):
    """Renders <script> tags pointing to the minify or nominify
    javascript views according to MINIFY_DEBUG setting
    
    Params:
    - files_in_string: a string of comma seperated Javascript file
    paths within app_settings.MINIFY_JS_PATH
    - from_url (optional): a url from a view within one of your
    apps or project without GET parameters (just the path),
    this view should return a response with mimetype=
    "text/javascript"
    """
    is_grouped = False
    script_paths = []
    
    if files_in_string.find('.js') == -1:
        #use a setting (app_settings.settings bcs from the global settings)
        files_array = getattr(app_settings.settings, files_in_string, [])
        if files_array and isinstance(files_array[0], (list, tuple)):
            is_grouped = True
    else:
        files_in_string = files_in_string.replace(' ','')
        files_array = files_in_string.split(',')
    
    if app_settings.MINIFY_DEBUG:
        base_url = NOMINIFY_JS_URL
    else:
        base_url = MINIFY_JS_URL
    
    construct_function = _get_construct_function()
    if is_grouped is False:
        script_paths = construct_function(base_url, files_array, from_url)
    else:
        if from_url:
            from_url_group = construct_function(base_url, [], from_url)
            script_paths.append(from_url_group)
        for file_group in files_array:
            script_group = construct_function(base_url, file_group)
            script_paths.append(script_group)
            
    return {
        'js_paths': script_paths,
        'is_grouped': is_grouped,
    }
    

@register.inclusion_tag('minify/css.html')
def css(files_in_string):
    """Renders <link> tags pointing to the minify or nominify
    CSS views according to MINIFY_DEBUG setting
    
    Params:
    - files_in_string: a string of comma seperated CSS file
    paths within app_settings.MINIFY_CSS_PATH
    """
    is_grouped = False
    css_paths = []
    
    if files_in_string.find('.css') == -1:
        #use a setting (app_settings.settings bcs from the global settings)
        files_array = getattr(app_settings.settings, files_in_string, [])
        if files_array and isinstance(files_array[0], (list, tuple)):
            is_grouped = True
    else:
        files_in_string = files_in_string.replace(' ','')
        files_array = files_in_string.split(',')
    
    if app_settings.MINIFY_DEBUG:
        base_url = NOMINIFY_CSS_URL
    else:
        base_url = MINIFY_CSS_URL
        
    construct_function = _get_construct_function()
    if is_grouped is False:
        css_paths = construct_function(base_url, files_array)
    else:
        for file_group in files_array:
            css_group = construct_function(base_url, file_group)
            css_paths.append(css_group)
    
    return {
        'css_paths': css_paths,
        'is_grouped': is_grouped,
    }
    

def _get_construct_function():
    """Utility function which return 
    the function to contruct minify url paths
    according to app_settings.MINIFY_DEBUG
    
    Returns:
    - the contruct function according to 
    app_settings.MINIFY_DEBUG
    """
    if app_settings.MINIFY_DEBUG is True:
        return _construct_nominify_paths
    return _construct_minify_paths

def _construct_nominify_paths(base_url, files_array, from_url=None):
    """Constructs the url paths pointing to
    files within minify which should not be minified.
    
    Params:
    - base_url: the url of pointing to the view either not
    minifying CSS or Javascript
    - files_array: a list of relative paths to files within
    app_settings.MINIFY_PATHS
    - from_url (optional): a url from a view within one of your
    apps or project without GET parameters (just the path),
    this view should return a response with mimetype=
    "text/javascript"
    
    Returns:
    - a list of url paths which should be used in the js/css
    templates to render script or link tags
    """
    url_paths = []
    if from_url:
        url_paths.append('%s?url=%s' % (base_url, from_url))
    for filename in files_array:
        if filename:
            url_paths.append('%s?file=%s' % (base_url, filename))
    return url_paths

def _construct_minify_paths(base_url, files_array, from_url=None):
    """Constructs the url paths pointing to
    files within minify which should be minified.
    
    Params:
    - base_url: the url of pointing to the view either not
    minifying CSS or Javascript
    - files_array: a list of relative paths to files within
    app_settings.MINIFY_PATHS
    - from_url (optional): a url from a view within one of your
    apps or project without GET parameters (just the path),
    this view should return a response with mimetype=
    "text/javascript"
    
    Returns:
    - a list of url paths which should be used in the js/css
    templates to render script or link tags
    """
    url_paths = []
    url_path = '%s?files=%s' % (base_url, ','.join(files_array))
    if from_url:
        url_paths.append('%s&url=%s' % (url_path, from_url))
    else:
        url_paths.append(url_path)
    return url_paths