.. _Python: http://www.python.org/
.. _Django: http://www.djangoproject.com/
.. _headJS: http://headjs.com/

=======================
django-minify
=======================

1. Requirements
:::::::::::::::::::::::::::::::::

At the moment *django-minify* requires Python_ >2.5 and
Django_ >1.0 to run.

2. Installation
:::::::::::::::::::::::::::::::::

Simply run:
::
    
    python setup.py install
    


You can also obtain django-minify via:

::
    
    pip install django-minify
    
or

::
    
    easy_install django-minify
    


3. Setup
:::::::::::::::::::::::::::::::::


If you want to use templatetags and run the tests
you need to add *django-minify* to your INSTALLED_APPS
setting:

::
    
    INSTALLED_APPS = (
        ...
        'minify',
        ...
    )
    

To use template tags you also need to copy minify directory in 
minify/templates/ to one of your template directories or add
minify/templates/ to your ``TEMPLATE_DIRS`` setting.


This doesn't let you use *django-minify* yet. Additionally you need
to add the setting ``MINIFY_PATHS`` to your project settings.
This must be a tuple or list providing directories *django-minify*
should look for files to minify and combine them. If you for example stored 
your JavaScript- and CSS-files in your ``MEDIA_ROOT`` you could do
something like this:

::
    
    MINIFY_PATHS = (
        os.path.join(MEDIA_ROOT, 'js'),
        os.path.join(MEDIA_ROOT, 'css')
    )  
    

You not necessarily need to use directories in your MEDIA_ROOT:

::
    
    MINIFY_PATHS = (
        os.path.join(os.path.dirname(__file__), 'javascript'),    # 'javascript' directory in project folder
        os.path.join(os.path.dirname(__file__), 'css'),    # 'css' directory in project folder
    )
    

Now the last thing to do is pointing to *django-minify* in
your main url conf. In project_dir/urls.py you can add:

::
    
    urlpatterns = patterns('',    
        ...
        (r'^minify/', include('minify.urls')),
        ...
    )
    

4. Usage
:::::::::::::::::::::::::::::::::

If you want specific files to be minified you can create
``<script>`` or ``<link>`` tags pointing to the *django-minify* views. 
Example assuming above url configuration is used:

::
    
    <link type="text/css" href="/minify/css/?files=reset.css,main.css" />
    <script type="text/javascript" src="/minify/js/?files=jquery/jquery-1.4.3.js,base.js"></script>
    

Though more comfortable to use are the *django-minify*
template tags. In your template do something like this:

::
    
    {% load minify_tags %}
    
    {% css "reset.css, main.css" %}
    {% js "jquery/jquery-1.4.3.js, base.js" %}
    

This will automatically render the ``<script>`` and ``<link>`` tags.
Also if you set DEBUG to True it will not combine and minify
the content of these files.


5. Complex usage
:::::::::::::::::::::::::::::::::

Sometimes you a have lot more than just a couple Javascript-
or CSS-files you want to use with *django-minify*. Instead
of specify them in your template you can create a setting for
it. The name of the setting doesn't matter. For example:

::
    
    MY_JAVASCRIPT_FILES = [
        'jquery/jquery-1.4.3.js',
        'jquery/jquery.tools.js',
        'base.js',
        'swfobject.js',
        ...
    ]
    
    
Then in your template you can simply use the name of the
setting instead of a comma-seperated string with all these
file paths in it:

::
    
    {% js "MY_JAVASCRIPT_FILES" %}
    

If you don't want to combine and minify all files together,
but for example group them you can use nested lists (or
tuples for that matter) in your setting:

::
    
    MY_JAVASCRIPT_FILES = [
        [
            'jquery/jquery-1.4.3.js',
            'jquery/jquery.tools.js'
        ],
        [
            'base.js',
            'swfobject.js'
        ]
    ]
    

This will combine and minify the files specified in the
first list/tuple and create a ``<script>`` tag for it, then
the files in the second group and so on. See the sample
project for a more complex example using headJS_.
    
One of your views is rendering JavaScript and you want
to minify this one as well? No problem. You can pass a
url as an optional parameter to your js template tag and
therefore to the view:

::
    
    {% load minify_tags %}
    
    {% js "jquery/jquery-1.4.3.js, base.js" "/url-path/to-my/js-view/" %}
    

The rendered script tag might then look something like this:

::
    
    <script src="/minify/js/?files=jquery/jquery-1.4.3.js,base.js&url=/url-path/to-my/js-view/"></script>
    

This will combine the Javascript prodided by your view with
the Javascript within these files. Keep in mind that in the
current version of *django-minify* the view content will be
appended first and after that the files will be combined with
it.


6. Additional settings
:::::::::::::::::::::::::::::::::

For *django-minify* you can provide a couple optional settings
to tweak it for your project. Within *django-minify* app there
are reasonable defaults set for it:

For example you could set debug mode just for *django-minify*

::
    
    # default: settings.DEBUG
    MINIFY_DEBUG = True #or False
    

Specify when browser cached CSS or Javascript will expire:

::
    
    # default: 5 (days)
    MINIFY_CSS_JS_EXPIRES = 3   # in days
    

Specify if HTTP-Response should set the ``Cache-Control`` header
to ``private`` or ``public``

::
    
    # default: False (cached in users browser and proxy cache)
    MINIFY_HEADER_CACHE_PRIVATE = True
    

Specify how long will minified content stay in Django's cache 
(if you use Django's cache framework):

::
    
    # default: 60*60*24*5 aka 5 days
    MINIFY_CACHE_DURATION = 300   # in seconds
    

 
    
    
