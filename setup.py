# coding=utf-8
import django_sae


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'django_sae',
    'django_sae.cache',
    'django_sae.contrib',
    'django_sae.contrib.tasks',
    'django_sae.db',
    'django_sae.utils',
]

requires = [
    'django>=1.6.2,<1.7',
    'sae-python-dev>=1.3.2',
]

with open('README.md') as f:
    readme = f.read()
with open('HISTORY.md') as f:
    history = f.read()

setup(
    name='django-sae',
    version=django_sae.__version__,
    description='for django in sae',
    long_description=readme + '\n\n' + history,
    author='smallcode',
    author_email='45945756@qq.com',
    url='https://github.com/smallcode/django-sae',
    packages=packages,
    package_dir={'django_sae': 'django_sae'},
    include_package_data=True,
    install_requires=requires,
    license=django_sae.__license__,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

