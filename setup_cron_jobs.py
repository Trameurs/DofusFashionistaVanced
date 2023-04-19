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

def main():
    call(['sudo', 'mkdir', '-p', '/var/log/fashionista'])
    call(['sudo', 'chmod', '777', '/var/log/fashionista'])
    
    print '== Setting up backup job =='
    print '== Setting up cleanup job =='
    call(['crontab', 'cronjobs_for_user.txt'])
    
    print '== Setting up auto restart job =='
    call(['sudo', 'crontab', 'cronjobs_for_root.txt'])

    print '== Printing user\'s cron jobs =='
    call(['crontab', '-l'])
    print '== Printing root\'s cron jobs =='
    call(['sudo', 'crontab', '-l'])
    
if __name__ == '__main__':
    main()
