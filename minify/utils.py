"""
Utility functions used to handle minifying
"""

import os
import urllib2

from django.core import urlresolvers

from jsmin import jsmin

from minify import app_settings

MINIFY_PATHS = app_settings.MINIFY_PATHS


def find_in_path(filename):
    """Utility function which is checking for given
    filename (with given subdirectories like "js/jquery.js")
    within in app_settings.MINIFY_PATHS.
    
    Params:
    - filename: the name of the file which is a relative
    path within app_settings.MINIFY_PATHS
    
    Returns:
    on success: - the valid and existing absolute path
    of the file within the file system
    on failure: None
    """
    for minify_path in MINIFY_PATHS:
        path = os.path.join(minify_path, filename)
        if os.path.exists(path) and os.path.isfile(path):
            return path
    return None

def read_from_file(file_path):
    """Utility function to read a file from
    a given absolute path.
    
    Params:
    - file_path: the absolute path of the file
    
    Returns:
    - the content of the file
    """
    file = open(file_path, 'r')
    file_content = file.read()
    file.close()
    return file_content

def check_and_read_from_file(request, filename):
    """Utility function which combine find_in_path
    and read_from_file functions. It first checks if
    a path for given filename exists and returns its
    absolute path. Then it reads the file and returns
    its content.
    If a given path starts with a '/' or points to a
    url via 'http://' the file content will be loaded
    using urllib2.urlopen.
    
    Params:
    - request: a django.http.HttpRequest object
    - filename: relative file path within app_settings.MINIFY_PATHS
    
    Returns:
    on success: content of the file
    on failure: empty string ''
    """
    if filename.startswith('/') or filename.startswith('http://'):
        if filename.startswith('/'):
            filename = 'http://%s%s' % (request.get_host(), filename)
        opener = urllib2.urlopen(filename)
        return opener.read()
    else:
        file_path = find_in_path(filename)
        if file_path is not None:
            return read_from_file(file_path)
    return ''

def minify_from_files(request, filenames, minifier):
    """Utility function to minify and combine a
    list of relative filenames within app_settings.MINIFY_PATHS
    
    Params:
    - request: a django.http.HttpRequest object
    - filenames: a list of relative filenames within
     app_settings.MINIFY_PATHS
     - minifier: the function which is used to minify the content
     
     Returns:
     - a the combined and minified content of files from filenames
    """
    minified_content = []
    for filename in filenames:
        file_content = check_and_read_from_file(request, filename)
        minified_content.append(minifier(file_content))
    return '\n'.join(minified_content)

def minify_js_from_files(request, filenames):
    """Minify and combine Javascript file content from
    given filenames.
    
    Params:
    - request: a django.http.HttpRequest object
    - filenames: a list of filenames or file paths within
    app_settings.MINIFY_JS_PATH
    
    Returns:
    - minified and combined content from Javascript files
    """
    return minify_from_files(request, filenames, minifier=minify_js)

def minify_css_from_files(request, filenames):
    """Minify and combine CSS file content from
    given filenames.
    
    Params:
    - request: a django.http.HttpRequest object
    - filenames: a list of filenames or file paths within
    app_settings.MINIFY_CSS_PATH
    
    Returns:
    - minified and combined content from CSS files
    """
    return minify_from_files(request, filenames, minifier=minify_css)

def minify_js(file_content):
    """Minifies Javascript content using JSMin
    
    Params:
    - filename: the filename of the Javascript file
    within app_settings.MINIFY_JS_PATH
    
    Returns:
    - minified Javascript content
    """
    return jsmin(file_content)

def minify_js_from_url(request, url, nominify=False):
    """Resolve a view given by the url and return and 
    minify its response content.
    
    Params:
    - request: a django.http.HttpRequest
    - url: url of a view which returns a text/javascript response
    - nominify: a flag if this response content should be
    minified or not
    
    Returns:
    - minified or not minified Javascript content from a view
    """
    url_split = request.GET['url'].split('?')
    url = url_split[0]
    query_string = None
    if len(url_split)>1:
        query_string = url_split[1]
    view, args, kwargs = urlresolvers.resolve(url)
    if query_string:
        request.GET = request.GET.copy() #make request.GET immutable
        for get_items in query_string.split('&'):
            get_key, get_value = get_items.split('=')
            request.GET[get_key] = get_value
    kwargs['request'] = request        
    if nominify is False:
        return jsmin(view(*args, **kwargs).content)
    else:
        return view(*args, **kwargs)

def minify_css(file_content):
    """Minifies CSS content
    
    Params:
    - filename: the filename of the css file
    within app_settings.MINIFY_CSS_PATH
    
    Returns:
    - minified CSS content
    """   
    return file_content.replace('\t', '').replace('\n', '').replace(', ', ',').replace(': ', ':').replace(' {', '{').replace('} ', '}')

def nominify_from_files(request, filenames):
    """Utilizes to explicitly not minifying the content
    of the files given in filenames.
    
    Params:
    - request: a django.http.HttpRequest object
    - filenames: a list of filenames or file paths within
    app_settings.MINIFY_CSS_PATH
    
    ReturnsL
    - combined but not minified file content from given
    files in filenames
    """
    not_minified_content = []
    for filename in filenames:
        file_content = check_and_read_from_file(request, filename)
        not_minified_content.append(file_content)
    return '\n'.join(not_minified_content)

def nominify_js_from_files(request, filenames):
    """Utility function to explicitly not minify
    Javascript, not used in minify app directly, but can be
    used by other apps which need it.
    
     Params:
     - request: a django.http.HttpRequest object
    - filenames: a list of filenames or file paths within
    app_settings.MINIFY_JS_PATH
    
    Returns:
    - not minified (but combined) Javascript
    """
    return nominify_from_files(request, filenames)

def nominify_css_from_files(request, filenames):
    """Utility function to explicitly not minify
    CSS, not used in minify app directly, but can be
    used by other apps which need it.
    
     Params:
     - request: a django.http.HttpRequest object
    - filenames: a list of filenames or file paths within
    app_settings.MINIFY_CSS_PATH
    
    Returns:
    - not minified (but combined) CSS
    """
    return nominify_from_files(request, filenames)
