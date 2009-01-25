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

from django_fuse import DirectoryResponse, FileResponse, WrappedFileResponse, \
    SymlinkResponse

def index():
    """
    Demonstrating a simple list-based directory index.
    """

    items = ['hostname', 'hostname.txt', 'subdir']
    return DirectoryResponse(items)

def hostname():
    """
    Demonstrating wrapping a request to a "real" file on the filesystem.
    """

    return WrappedFileResponse('/etc/hostname')

def hostname_symlink():
    """
    Demonstrating returning a symlink.
    """

    return SymlinkResponse('/etc/hostname')

def subdir():
    """
    Demonstrating a generator-based approach to populating a directory
    index. The use of a count callback function is an optimisation to
    prevent evaluation of the generator when displaying the file in a
    directory index.

    Imagine replacing these static results with ones based on a QuerySet-
    based database query. You may wish to use itertools.imap to lazily
    format the filename before returning it.
    """

    def items():
        for letter in "abc":
            yield "%s.txt" % letter

    def count_cb():
        return 3

    return DirectoryResponse(items, count_cb)

def letter_file(letter):
    """
    Demonstrating using the Django templating system to create a faux
    file with dynamic contents.
    """

    from django.template import Context, Template

    t = Template("""This is {{ letter }}.txt\n""")
    c = Context({'letter': letter})

    return FileResponse(t.render(c))
