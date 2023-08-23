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

# Warning: black magic ahead

import base64
import hashlib
from django.conf import settings

SECRET_PART_1 = settings.GEN_CONFIGS['char_id_SECRET_PART_1']
SECRET_PART_2 = settings.GEN_CONFIGS['char_id_SECRET_PART_2']
URL_SAFE_BASE_64_ENCODE = str.maketrans('+/=', '.-_')
URL_SAFE_BASE_64_DECODE = str.maketrans('.-_', '+/=')

def _sign(char_id):
    data_to_sign = "{}{}{}".format(SECRET_PART_1, char_id, SECRET_PART_2).encode('utf-8')
    return hashlib.sha1(data_to_sign).digest()[:4]

def encode_char_id(char_id):
    combined_data = str(char_id).encode('utf-8') + _sign(char_id)
    encoded_bytes = base64.b64encode(combined_data)
    return encoded_bytes.decode('utf-8').translate(URL_SAFE_BASE_64_ENCODE)
    
def decode_char_id(encoded_char_id):
    half_decoded_id = base64.b64decode(str(encoded_char_id).translate(URL_SAFE_BASE_64_DECODE))
    try:
        candidate_id = int(half_decoded_id[:-4].decode('utf-8'))
    except ValueError:
        return None
    signature = half_decoded_id[-4:]
    if signature != _sign(candidate_id):
        return None
    return candidate_id
