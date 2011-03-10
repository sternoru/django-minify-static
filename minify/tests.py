import unittest
import os

from django.test import client
from django.core import urlresolvers

from minify import app_settings


class MinifyTestCase(unittest.TestCase):
    def setUp(self):
        sample_js_files = []
        sample_css_files = []
        for path in app_settings.MINIFY_PATHS:
            for t in os.walk(path):
                dirname = t[0].replace(path, '').lstrip('/')
                for filename in t[2]:
                    if filename.endswith('.js'):
                        if dirname:
                            sample_js_files.append('%s/%s' % (dirname, filename))
                        else:
                            sample_js_files.append(filename)
                    elif filename.endswith('.css'):
                        if dirname:
                            sample_css_files.append('%s/%s' % (dirname, filename))
                        else:
                            sample_css_files.append(filename)
        self.javascript_files = sample_js_files
        self.css_files = sample_css_files
        self.minify_js_url = urlresolvers.reverse('minify_js')
        self.minify_css_url = urlresolvers.reverse('minify_css')
        self.nominify_js_url = urlresolvers.reverse('nominify_js')
        self.nominify_css_url = urlresolvers.reverse('nominify_css')
    
    def test_minify_js_view(self):
        c = client.Client()
        response = c.get(self.minify_js_url, {'files': ','.join(self.javascript_files)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('text/javascript' in response['Content-Type'])
        self.assertTrue(len(response.content) > 0)
    
    def test_minify_css_view(self):
        c = client.Client()
        response = c.get(self.minify_css_url, {'files': ','.join(self.css_files)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('text/css' in response['Content-Type'])
        self.assertTrue(len(response.content) > 0)
    
    def test_nominify_js_view(self):
        c = client.Client()
        for js_file in self.javascript_files:
            response = c.get(self.nominify_js_url, {'file': js_file})
            self.assertEqual(response.status_code, 200)
            self.assertTrue('text/javascript' in response['Content-Type'])
            self.assertTrue(len(response.content) > 0)
    
    def test_nominify_css_view(self):
        c = client.Client()
        for css_file in self.css_files:
            response = c.get(self.nominify_css_url, {'file': css_file})
            self.assertEqual(response.status_code, 200)
            self.assertTrue('text/css' in response['Content-Type'])
            print response.content
            self.assertTrue(len(response.content) > 0)
    

