# -*- coding: utf-8 -*-

# django-fuse -- FUSE adaptor for Django
# Copyright (C) 2008 Chris Lamb <chris@chris-lamb.co.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import fuse
import errno

from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404

fuse.fuse_python_api = (0, 2)
fuse.feature_assert('stateful_files')

__all__ = ('DjangoFs',)

def render(fn):
    def wrapped(self, path, *args, **kwargs):
        try:
            # Resolve requested URL to a view and "render" it.
            view_fn, view_args, view_kwargs = \
                resolve(path, urlconf=settings.FUSE_URLCONF)
            response = view_fn(*view_args, **view_kwargs)

            # Pass the response as the first argument, replacing
            # 'path' from the callsite in fuse.py
            return fn(self, response, *args, **kwargs)

        except Resolver404:
            # Path does not exist
            return -errno.ENOENT

    return wrapped

class DjangoFs(fuse.Fuse):
    @render
    def getattr(self, response):
        return response.getattr()

    @render
    def readdir(self, response, offset):
        return response.readdir()

    @render
    def open(self, response, flags):
        return response.open(flags)

    @render
    def unlink(self, response):
        return -errno.EACCES

    @render
    def access(self, response, mode):
        if mode & os.W_OK:
            return -errno.EACCES
        return 0

    @render
    def rename(self, response, target):
        return -errno.EACCES

    @render
    def readlink(self, response):
        return response.readlink()

    # Stateful-file calls - no need to route them as we have already created
    # a stateful object fileobj for these.

    def read(self, path, length, offset, fileobj):
        return fileobj.read(length, offset)

    def release(self, path, flags, fileobj):
        return fileobj.release()
