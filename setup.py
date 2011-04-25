from setuptools import setup, find_packages

setup(
      name='django-minify',
      version='0.1',
      description='Application to minify static file content for Django',
      author='Sterno.Ru',
      author_email='sterno.beijing@gmail.com',
      url='',
      download_url='',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
        'Environment :: Web Environment',
        "Programming Language :: Python",
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)