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

import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from chardata.model_wrappers import WrappedChar
from chardata.models import Char
from chardata.solution import get_solution
from chardata.util import set_response, get_theme
from static_s3.templatetags.static_s3 import static
from chardata.themes import get_needle_URL


def load_projects(request, char_id=0):
    return load_projects_error(request, error=None)

def load_projects_error(request, error):
    chars = []
    if request.user is not None and not request.user.is_anonymous():
        chars = Char.objects.filter(owner=request.user)
        chars = chars.exclude(deleted=True)
    has_projects = False
    if len(chars) > 0:
        has_projects = True
    if request.user.is_anonymous() and 'char_id' in request.session:
        char = get_object_or_404(Char, pk=request.session['char_id'])
        chars.append(char)
        has_projects = True

    return set_response(request, 
                        'chardata/load_projects.html',
                        {'chars': [WrappedChar(char) for char in chars],
                         'char_id': 0,
                         'has_projects': has_projects,
                         'needle': json.dumps(get_needle_URL(request)),
                         'error_msg': error})

def user_has_projects(request):
    chars = []
    if request.user is not None and not request.user.is_anonymous():
        chars = Char.objects.filter(owner=request.user)
        chars = chars.exclude(deleted=True)
    has_projects = False
    if len(chars) > 0:
        has_projects = True
    if request.user.is_anonymous() and 'char_id' in request.session:
        char = get_object_or_404(Char, pk=request.session['char_id'])
        chars.append(char)
        has_projects = True
    return has_projects

def load_a_project(request, char_id):
    char = get_object_or_404(Char, pk=char_id)
    if get_solution(char) is not None:
        return HttpResponseRedirect(reverse('chardata.solution_view.solution', args=(char.id,)))
    return HttpResponseRedirect(reverse('chardata.wizard_view.wizard', args=(char.id,)))
                                              
def infeasible(request, char_id=0):
    char = get_object_or_404(Char, pk=char_id)
    return set_response(request, 
                        'chardata/infeasible.html', 
                        {'request': request,
                         'user': request.user,
                         'char_id': char_id,
                         'mins_link': reverse('chardata.min_stats_view.min_stats', args=(char_id,)),
                         'weights_link': reverse('chardata.stats_weights_view.stats', args=(char_id,)),
                         'lock_link': reverse('chardata.inclusions_view.inclusions', args=(char_id,)),
                         'exo_link': reverse('chardata.options_view.options', args=(char_id,))},
                        char)
                                                         
def forbidden(request, char_id=0):
    return set_response(request, 
                        'chardata/403.html', 
                        {'request': request,
                         'user': request.user,
                         'char_id': char_id})
                         
def not_found(request, char_id=0):
    return set_response(request, 
                        'chardata/404.html', 
                        {'request': request,
                         'user': request.user,
                         'char_id': char_id})
                                                        
def app_error(request, char_id=0):
    return set_response(request, 
                        'chardata/500.html', 
                        {'request': request,
                         'user': request.user,
                         'char_id': char_id})
                                                        
def contact(request, char_id=0):
    return set_response(request, 
                        'chardata/contact.html', 
                        {'request': request,
                         'user': request.user,
                         'char_id': char_id})

def about(request, char_id=0):
    return set_response(request, 
                        'chardata/about.html', 
                        {'request': request,
                         'user': request.user,
                         'char_id': char_id,
                         'site_version': settings.SITE_VERSION})

def license_page(request, char_id=0):
    return set_response(request, 
                        'chardata/license.html', 
                        {'request': request,
                         'user': request.user,
                         'char_id': char_id})

def faq(request, char_id=0):
    return set_response(request, 
                        'chardata/faq.html', 
                        {'request': request,
                         'user': request.user,
                         'char_id': char_id})
