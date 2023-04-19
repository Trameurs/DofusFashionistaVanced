#!/usr/bin/env python

# Copyright (C) 2020 The Dofus Fashionista
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import getpass
from subprocess import call

def main():
    if getpass.getuser() == 'root':
        print 'Run this script as a regular user, not as root.'
        return

    _print_header('Creating database')
    call(['mysql', '-e', 'CREATE DATABASE IF NOT EXISTS fashionista;'])

    _print_header('Syncing db')
    call(['python', 'fashionsite/manage.py', 'syncdb'])
    call(['python', 'fashionsite/manage.py', 'migrate', 'chardata'])
    call(['chmod', '777', 'fashionsite'])

    _print_header('Done')

def _print_header(header):
    print '=' * 60
    print header
    print '=' * 60

if __name__ == '__main__':
    main()
