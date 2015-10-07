from setuptools import setup, find_packages

setup(
    name='django-fuse',

    url="https://chris-lamb.co.uk/projects/django-fuse",
    version='2',
    description="Abstractions for building FUSE filesystems using Django",

    author="Chris Lamb",
    author_email='chris@chris-lamb.co.uk',
    license="BSD",

    packages=find_packages(),
)
