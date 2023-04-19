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

import argparse
import getpass
import json
import os
from subprocess import call

CONFIG_DIR = '/etc/fashionista'

APT_GET_PACKAGES_TO_INSTALL = [
    'python-pip', # Package manager.
    'sqlite3', # Database.
    #'apache2', # Web server.
    #'libapache2-mod-wsgi', # Apache-Django interface.
    'pngcrush', # Image optimizer.
    'imagemagick', # Image processing to resize assets.
    'mysql-server',
    'mysql-client',
    'python-dev',
    'libmysqlclient-dev',
    'libevent-dev',
    'memcached',
]

PIP_PACKAGES_TO_INSTALL = [
    'Django==1.8.13.....', # Application server.
    'python-social-auth==0.2.21', # Federated SSO.
    'social-auth-core',
    'social-auth-app-django',
    'PuLP', # Bindings for LP solver.
    'Scrapy', # Web crawler.
    'jsonpickle', # Powerful json encoder for ajax.
    'django-htmlmin', # Minifier for HTML.
    'boto', # S3 client for uploading db.
    'MySQL-python',
    'python-memcached',
    'django-sslserver',
    'unidecode',
]

GEN_CONFIG_FILE = {
    'PASSWORD_RESET_SALT': 'my_salt',
    'EMAIL_CONFIRMATION_SALT': 'my_salt_2',
    'SECRET_KEY': 'my_secret_key',
    "mysql_PASSWORD": "my_password",
    "mysql_USER": "root", 
    'EMAIL_HOST_USER': "my_username",
    'EMAIL_HOST_PASSWORD': "my_password",
    'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY': None,
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET': None,
    'SOCIAL_AUTH_FACEBOOK_KEY': None,
    'SOCIAL_AUTH_FACEBOOK_SECRET': None,
    'DBBACKUP_S3_ACCESS_KEY': None,
    'DBBACKUP_S3_SECRET_KEY': None,
    'url_captcha_secret': None,
    'char_id_SECRET_PART_1': 'my_secret',
    'char_id_SECRET_PART_2': 'my_other_secret',
    'google_analytics_id': None,
    'TESTER_USERS_EMAILS': ["my_email@here.com"],
    'SUPER_USERS_EMAILS': [],
    "EMAIL_USE_TLS": True,
    "EMAIL_HOST": "smtp@host.com",
    "EMAIL_PORT": 587,
    }

def main():
    if getpass.getuser() != 'root':
        print 'Run this script as root.'
        return
        
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--install_deps',
                        action='store_true',
                        help='install packages Fashionista depends on')
    parser.add_argument('-s', '--serve_static_files',
                        action='store_true',
                        help='serve static files instead of linking to S3')
    parser.add_argument('-d', '--debug_mode',
                        action='store_true',
                        help='run server in DEBUG mode')
    args = parser.parse_args()
    
    _print_header('Writing config files')
    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
        
    path_config_file_path = CONFIG_DIR + '/config'
    with open(path_config_file_path, 'w') as f:
        f.write(os.getcwd())
    print 'Wrote path to %s' % path_config_file_path
    
    path_gen_config_file_path = CONFIG_DIR + '/gen_config.json'
    if not os.path.exists(path_gen_config_file_path):
        with open(path_gen_config_file_path, 'w') as f:
            f.write(json.dumps(GEN_CONFIG_FILE, indent=4, sort_keys=True))
        print 'Wrote path to %s. Please fill it out manually.' % path_gen_config_file_path
        raw_input('Press Enter once it is done.')
    else:
        print 'Skipping creation of %s: already exists.' % path_config_file_path
    
    static_config_file_path = CONFIG_DIR + '/serve_static'
    with open(static_config_file_path, 'w') as f:
        f.write(str(args.serve_static_files))
    print 'Wrote serve static to %s' % static_config_file_path

    debug_config_file_path = CONFIG_DIR + '/debug_mode'
    with open(debug_config_file_path, 'w') as f:
        f.write(str(args.debug_mode))
    print 'Wrote debug mode to %s' % debug_config_file_path

    with open(path_gen_config_file_path, 'r') as f:
        GEN_CONFIGS = json.loads(f.read())
    mysql_config_file_path = '../.my.cnf'
    with open(mysql_config_file_path, 'w') as f:
        f.write("""
[client]
user=%s
password=%s

[mysqldump]
user=%s
password=%s
""" % (GEN_CONFIGS['mysql_USER'], 
       GEN_CONFIGS['mysql_PASSWORD'], 
       GEN_CONFIGS['mysql_USER'], 
       GEN_CONFIGS['mysql_PASSWORD']))
    call(['chmod', '644', mysql_config_file_path])
    print 'Wrote MySQL config to %s' % mysql_config_file_path

    if args.install_deps:
        _print_header('Installing dependencies')
        call(['apt-get', 'install'] + APT_GET_PACKAGES_TO_INSTALL)
        call(['python', '-m', 'pip', 'install'] + PIP_PACKAGES_TO_INSTALL);

    _print_header('Done')

def _print_header(header):
    print '=' * 60
    print header
    print '=' * 60

if __name__ == '__main__':
    main()
