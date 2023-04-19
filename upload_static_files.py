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

import os
import csv
from subprocess import call
import s3_fashionista

STATIC_ROOT = '/tmp/statictemp'
DBBACKUP_S3_BUCKET = 'fash-static'

def main():
    with open('/etc/fashionista/serve_static') as f:
        serve_static = f.read().startswith('True')
        if not serve_static:
            print 'Fashionista needs to be configured with serve_static=True'
            exit(1)

    call(['rm', '-rf', STATIC_ROOT])

    old_map = {}
    with open('static_file_map.csv', 'rb') as file_map_old:
        csvreader = csv.reader(file_map_old)
        for row in csvreader:
            if len(row) > 0:
                old_map[row[0]] = row[1]
    
    new_map = {}
    keys = []
    with open('static_file_map.csv', 'wb') as file_map:
    
        os.chdir('fashionsite')
        call(['python', 'manage.py', 'collectstatic'])
        
        csvwriter = csv.writer(file_map)
    
        os.chdir(STATIC_ROOT)
        for root, subdirs, files in os.walk(STATIC_ROOT):
            for file_name in files:
                pieces = file_name.split('.')
                if len(pieces) >= 3:
                    len_pieces = len(pieces)
                    original = os.path.relpath(root, start=STATIC_ROOT) + '/'
                    new = os.path.relpath(root, start=STATIC_ROOT) + '/'
                    for i in range(0, len_pieces-2):
                        original += pieces[i] + '.'
                        new += pieces[i] + '.'
                    original += pieces[len_pieces-1]
                    new += pieces[len_pieces-2] + '.' + pieces[len_pieces-1]                
                    keys.append(original)
                    new_map[original] = new
        
        keys.sort()
        for original_name in keys:
            csvwriter.writerow([original_name, new_map[original_name]])
        
        bucket = s3_fashionista.get_s3_bucket(DBBACKUP_S3_BUCKET)
        for (original_name, new_name) in new_map.iteritems():
            if original_name not in old_map:
                print 'Uploading ' + original_name + ': not in original map'
                key = bucket.new_key(new_name)
                key.set_contents_from_filename(new_name, cb=_update_progress, num_cb=1)
            else:
                if old_map[original_name] != new_map[original_name]:
                    print 'Uploading ' + original_name + ': Hash changed'
                    key = bucket.new_key(new_name)
                    key.set_contents_from_filename(new_name, cb=_update_progress, num_cb=1)

def _update_progress(so_far, total):
   print '%d bytes transferred out of %d' % (so_far, total)
              
if __name__ == '__main__':
    main()
