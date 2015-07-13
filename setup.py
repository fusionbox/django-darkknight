#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(name='django-darkknight',
      version='0.9.0',
      license="BSD",
      description="He's a silent guardian, a watchful protector",
      long_description=read('README.rst'),

      author="Fusionbox, Inc",
      author_email="programmers@fusionbox.com",

      url='http://github.com/fusionbox/django-darkknight',

      packages=['darkknight', 'darkknight_gpg'],
      install_requires=[
          'django-dotenv',
          'Django>=1.5',
          'pyOpenSSL',
          'django-localflavor',
          'django-countries',
      ],
      extras_require = {
          'gpg': ['gnupg>=2.0.2,<3', 'django-apptemplates'],
      },

      classifiers=[
          "Development Status :: 4 - Beta",
          "Framework :: Django",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "Topic :: Security :: Cryptography",
      ],

      )
