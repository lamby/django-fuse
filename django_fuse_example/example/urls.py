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

from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
   url(r'^$', views.index),
   url(r'^hostname$', views.hostname_symlink),
   url(r'^hostname\.txt$', views.hostname),
   url(r'^subdir$', views.subdir),
   url(r'^subdir/(a|b|c)\.txt$', views.letter_file),
)
