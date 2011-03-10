"""
App specific settings for minify
"""

from django.conf import settings

MINIFY_DEBUG = getattr(settings, 'MINIFY_DEBUG', settings.DEBUG)
MINIFY_PATHS = getattr(settings, 'MINIFY_PATHS', [])
#in days
MINIFY_CSS_JS_EXPIRES = getattr(settings, 'MINIFY_CSS_JS_EXPIRES', 5)
MINIFY_HEADER_CACHE_PRIVATE = getattr(settings, 'MINIFY_HEADER_CACHE_PRIVATE', False)
#in seconds
MINIFY_CACHE_DURATION = getattr(settings, 'MINIFY_CACHE_DURATION', 60*60*24*5)
