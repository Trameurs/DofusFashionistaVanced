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

from boto.s3.connection import S3Connection
import json

with open('/etc/fashionista/gen_config.json', 'r') as f:
    GEN_CONFIGS = json.loads(f.read())
DBBACKUP_S3_ACCESS_KEY = GEN_CONFIGS['DBBACKUP_S3_ACCESS_KEY']
DBBACKUP_S3_SECRET_KEY = GEN_CONFIGS['DBBACKUP_S3_SECRET_KEY']

def get_s3_bucket(bucket):
    conn = S3Connection(DBBACKUP_S3_ACCESS_KEY, DBBACKUP_S3_SECRET_KEY)
    return conn.get_bucket(bucket)

