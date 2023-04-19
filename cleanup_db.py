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

import datetime
import os
import sys

sys.path.append('fashionsite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashionsite.settings')

import django
django.setup()

from chardata.models import Char, SolutionCounter, SolutionMemory

DRY_RUN = False

DELETE_UP_TO_DELETED_PROJECTS = 3000
KEEP_DELETED_FOR_DAYS = 60

DELETE_UP_TO_ORPHAN_PROJECTS = 2000
KEEP_ORPHAN_FOR_DAYS = 90

CACHED_SOLUTION_CONSOLIDATES_AFTER_TIMES = 4
KEEP_ANY_SOLUTIONS_CACHED_FOR_DAYS = 2

def main():
    print_with_time('Cleaning up database.')
    if DRY_RUN:
        print_with_time('This is a dry run. Nothing will be done.')

    remove_deleted_chars()
    remove_orphan_chars()
    remove_cached_solutions()

def remove_deleted_chars():
    # Removing deleted projects.
    end_date = date_with_days_ago(KEEP_DELETED_FOR_DAYS)
    print_with_time('Removing projects deleted before %s' % end_date)
    
    chars_to_delete = Char.objects.filter(deleted=True, 
                                          modified_time__lte=end_date)[:DELETE_UP_TO_DELETED_PROJECTS]
    char_ids_to_delete = map_ids(chars_to_delete)
    print_with_time('Number of projects to be deleted: %d' % len(char_ids_to_delete))
    delete_char_projects(char_ids_to_delete)
        
def remove_orphan_chars():
    # Removing old projects without owners.
    end_date = date_with_days_ago(KEEP_ORPHAN_FOR_DAYS)
    print_with_time('Removing orphan projects modified before %s' % end_date)
    
    chars_to_delete = Char.objects.filter(owner=None, 
                                          modified_time__lte=end_date)[:DELETE_UP_TO_ORPHAN_PROJECTS]
    char_ids_to_delete = map_ids(chars_to_delete)
    print_with_time('Number of orphan projects to be deleted: %d' % len(char_ids_to_delete))
    delete_char_projects(char_ids_to_delete)

def remove_cached_solutions():
    # Removing cached solutions used only a few times and not very recently. 
    end_date = date_with_days_ago(KEEP_ANY_SOLUTIONS_CACHED_FOR_DAYS)
    print_with_time('Removing cached solutions less than %d times, and not since %s'
                    % (CACHED_SOLUTION_CONSOLIDATES_AFTER_TIMES, end_date))
    sc_to_delete = SolutionCounter.objects.filter(modified_time__lte=end_date,
                                                  get_count__lt=CACHED_SOLUTION_CONSOLIDATES_AFTER_TIMES)
    hashes_to_delete = sc_to_delete.values_list('input_hash', flat=True)
    cs_to_delete = SolutionMemory.objects.filter(input_hash__in=hashes_to_delete)
    cs_ids_to_delete = map_ids(cs_to_delete)
    print_with_time('Number of cached solutions to be deleted: %d' % len(cs_ids_to_delete))
    delete_cached_solutions(cs_ids_to_delete)


def date_with_days_ago(days_ago):
    return datetime.date.today() - datetime.timedelta(days=days_ago)

def map_ids(models):
    return models.values_list('id', flat=True)

def delete_char_projects(char_ids_to_delete):
    if DRY_RUN:
        print_with_time('Would be deleting projects, but it\'s a dry run')
    else:
        print_with_time('Deleting projects')
        Char.objects.filter(pk__in=list(char_ids_to_delete)).delete()

def delete_cached_solutions(cs_ids_to_delete):
    if DRY_RUN:
        print_with_time('Would be deleting cached solutions, but it\'s a dry run')
    else:
        print_with_time('Deleting cached solutions')
        SolutionMemory.objects.filter(pk__in=list(cs_ids_to_delete)).delete()

def print_with_time(s):
    print '[%s] %s' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s)

if __name__ == '__main__':
    main()
