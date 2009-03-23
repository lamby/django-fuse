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
import stat
import errno

from django_fuse.utils import DefaultStat

__all__ = ('DirectoryResponse', 'FileResponse', 'WrappedFileResponse', 'SymlinkResponse')

class DirectoryResponse(object):
    def __init__(self, items=(), count=None, mode=0555):
        self.items = items
        self.count = count
        self.mode = mode

    def getattr(self):
        st = DefaultStat()
        st.st_mode = stat.S_IFDIR | self.mode

        if self.count:
            if callable(self.count):
                st.st_nlink = 2 + self.count()
            else:
                st.st_nlink = 2 + self.count
        else:
            # Set a fallback nlink
            st.st_nlink = 1

        return st

    def readdir(self):
        yield fuse.Direntry('.')
        yield fuse.Direntry('..')

        if callable(self.items):
            items = self.items()
        else:
            items = self.items

        for name in items:
            if isinstance(name, unicode):
                yield fuse.Direntry(name.encode('utf-8'))
            else:
                yield fuse.Direntry(name)

class AbstractFileResponse(object):
    def __init__(self, mode=0444):
        self.mode = mode

    def read(self):
        raise NotImplemented()

    def getattr(self):
        raise NotImplemented()

    def release(self):
        pass

    def open(self, flags):
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES

        return self.get_file_obj(flags)

    def get_file_obj(self, flags):
        return self

class FileResponse(AbstractFileResponse):
    def __init__(self, contents):
        super(FileResponse, self).__init__()
        self.contents = contents.encode('utf8')

    def getattr(self):
        st = DefaultStat()
        st.st_mode = stat.S_IFREG | self.mode
        st.st_size = len(self.contents)
        st.st_nlink = 1
        return st

    def read(self, length, offset):
        return self.contents[offset:offset + length]

class WrappedFileResponse(AbstractFileResponse):
    def __init__(self, filename):
        super(WrappedFileResponse, self).__init__()
        self.filename = filename

    def get_file_obj(self, flags):
        self.file = os.fdopen(os.open(self.filename, flags))
        return self

    def getattr(self):
        return os.lstat(self.filename)

    def read(self, length, offset):
        self.file.seek(offset)
        return self.file.read(length)

    def release(self):
        self.file.close()

    def fgetattr(self):
        return os.fstat(self.file.fileno())

class SymlinkResponse(object):
    def __init__(self, target):
        self.target = target

    def getattr(self):
        st = DefaultStat()
        st.st_mode = stat.S_IFLNK | 0777
        return st

    def readlink(self):
        return self.target.encode('utf-8')
