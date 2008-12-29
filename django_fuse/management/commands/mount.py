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

import sys
import fuse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django_fuse.fs import DjangoFs

class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.fs = DjangoFs(usage='%prog mount [mountpoint] [options]')
        self.fs.parser.add_options(BaseCommand.option_list)

    def handle(self, *args, **options):
        if getattr(settings, 'FUSE_URLCONF', None) is None:
            raise CommandError("You need to set FUSE_URLCONF to use django-fuse.")

        try:
            self.fs.main()
        except fuse.FuseError:
            sys.exit(1)

    def create_parser(self, prog_name, subcommand):
        # Proxy fuse.py's parser object
        return self.fs.parser
