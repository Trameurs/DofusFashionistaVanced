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

from PIL import Image
import argparse
import os
import subprocess
import sys


def convert_image(folder, item, new_folder):
    print 'convert_image(%s, %s, %s)' % (folder, item, new_folder)
    file_path = os.path.join(folder, item)
    if os.path.isfile(file_path):
        file_name_without_ext, e = os.path.splitext(item)
        if e.lower() == '.webp':
            new_file_path = '%s/%s%s' % (new_folder, file_name_without_ext, '.png')
            command = ['dwebp', file_path, '-o', new_file_path]
            print 'Writing %s' % new_file_path
            subprocess.call(command)

def convert_file_list(file_list):
    for file_path in file_list:
        folder, file_name = os.path.split(file_path)
        new_folder = get_new_folder_that_exists(folder)
        convert_image(folder, file_name, new_folder)

def convert_all():
    for folder in FOLDERS:
        new_folder = get_new_folder_that_exists(folder)
        dirs = os.listdir(folder)
        for item in dirs:
            convert_image(folder, item, new_folder)

def get_new_folder_that_exists(folder):
    new_folder = os.path.join(folder, 'png')
    subprocess.call(['mkdir', '-p', new_folder])
    return new_folder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='FILE', type=str, nargs='*',
                        help='files to be converted')
    args = parser.parse_args()
    
    if args.files:
        convert_file_list(args.files)
    else:
        convert_all()

if __name__ == '__main__':
    main()


