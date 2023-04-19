import csv
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static as built_in_static

from fashionistapulp.fashionista_config import serve_static_files, get_fashionista_path

register = template.Library()

SERVING_STATIC = serve_static_files()

@register.simple_tag
def static(path, astr=None, name=None):
    if '[!]' in path:
        return None
    if SERVING_STATIC:
        return built_in_static(path)
    else:
        mapped_file = _get_mapped_file(path)
        if mapped_file is not None:
            return built_in_static(mapped_file)
        else:
            return None

file_map = None
def _get_mapped_file(path):
    global file_map
    if file_map is None:
        file_map = {}
        file_map_file_path = get_fashionista_path() + '/static_file_map.csv'
        with open(file_map_file_path, 'rb') as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                file_map[row[0]] = row[1]

    new_path = file_map.get(path)
    if new_path == None:
        print 'Static file path not found:'
        print path
    return new_path
