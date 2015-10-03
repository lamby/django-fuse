# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-fuse',
    version=1,
    packages=[
        'django_fuse',
        'django_fuse.management',
        'django_fuse.management.commands',
    ],
)
