import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = ['django==1.8']

setup(
    name='django-stars',
    version='0.1',
    packages=['stars'],
    include_package_data=True,
    license='MIT License',
    description='A simple Django app to store object ratings.',
    long_description=README,
    url='https://github.com/djangothon/dajngo-stars',
    author='Chandan Singh, Ravi Ojha',
    author_email='singh.chandan4455@gmail.com, raviojha2105@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)