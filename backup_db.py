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

from subprocess import call
import datetime
import os
import platform
import time

import s3_fashionista

TEMP_LOCATION = '/tmp/'
DBBACKUP_S3_BUCKET = 'fashionista-dbbackup'
MYSQL_DB_NAME = 'fashionista'

def main():
    print '[%s]' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    backup_file_radical = _get_filename()
    backup_file = backup_file_radical + '.dump'
    backup_file_path = TEMP_LOCATION + backup_file
    print 'Writing backup file to %s' % backup_file_path
    
    os.system('mysqldump %s > %s' % (MYSQL_DB_NAME, backup_file_path))
    
    backup_file_zipped = backup_file + '.gz'
    backup_file_zipped_path = TEMP_LOCATION + backup_file_zipped
    print 'GZipping to %s' % backup_file_zipped
    call(['gzip', backup_file_path])
    
    print 'Uploading to S3 bucket %s' % DBBACKUP_S3_BUCKET
    bucket = s3_fashionista.get_s3_bucket(DBBACKUP_S3_BUCKET)
    key = bucket.new_key(backup_file_zipped)
    key.set_contents_from_filename(backup_file_zipped_path, cb=_update_progress, num_cb=5)
    
    print 'Deleting backup file from %s' % backup_file_path
    call(['rm', backup_file_zipped_path])

def _get_filename():
    return 'backup-%s-%s' % (platform.node(),
                             time.strftime("%Y-%m-%d-%H-%M-%S"))

def _update_progress(so_far, total):
   print '%d bytes transferred out of %d' % (so_far, total)

if __name__ == '__main__':
    main()
