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

ROOT_DIR = 'fashionsite/chardata/static/chardata'
TMP_FILE = 'tmp_pngcrush.png'
PROCESSED_FILE = 'optimized_images.csv'

import csv
import hashlib
import os
import subprocess

def main():
    files_there = []
    processed_files = {}
    if os.path.isfile(PROCESSED_FILE):
        with open(PROCESSED_FILE) as processed_file:
            for row in csv.reader(processed_file):
                processed_files[row[0]] = row[1]
    
    for root, subdirs, files in os.walk(ROOT_DIR):
        for file_name in files:
            if not file_name.endswith('.png'):
                continue

            f_path = os.path.join(root, file_name)
            files_there.append(f_path)                
            
            if processed_files.get(f_path, None) == get_md5_of_file(f_path):
                continue
            
            size_before = os.path.getsize(f_path)
            try:
                subprocess.call(['pngcrush', '-q', f_path, TMP_FILE])
                os.remove(f_path)
                os.rename(TMP_FILE, f_path)
            except:
                pass
            size_after = os.path.getsize(f_path)
            print ('[%s] Crushed from %d to %d bytes (%.2f%% reduction)'
                   % (f_path, size_before, size_after,
                      (size_before - size_after) / (float(size_before))))
            processed_files[f_path] = get_md5_of_file(f_path)

    files_there.sort()
    with open(PROCESSED_FILE, 'wb') as processed_file:
        writer = csv.writer(processed_file)
        for file_there in files_there:
            writer.writerow([file_there, processed_files[file_there]])

def get_md5_of_file(file_name):
    with open(file_name) as f:
        file_contents = f.read()
        return hashlib.md5(file_contents).hexdigest()

if __name__ == '__main__':
    main()
