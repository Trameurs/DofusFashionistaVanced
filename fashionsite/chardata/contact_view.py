# -*- coding: utf-8 -*-

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

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from chardata.models import ContactForm
from django.core.mail import send_mail, BadHeaderError
from chardata.util import set_response
import urllib2
import json

def contact(request):
    return set_response(request,
                        'chardata/contacts.html',
                        {'form': ContactForm()})

def send_email(request):
    subject = request.POST.get('topic', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    name = request.POST.get('name', '')
    g_recaptcha_response = request.POST.get('g-recaptcha-response', '')
    
    url = ("https://www.google.com/recaptcha/api/siteverify?secret=%s&response=%s" 
           % (settings.GEN_CONFIGS['url_captcha_secret'], g_recaptcha_response))
    
    is_bot_json = urllib2.urlopen(url).read(1000)
    
    is_bot = json.loads(is_bot_json)
    if is_bot['success'] == 1:
    
        try:
            send_mail("Fashionista Form: " + subject, 
                      message + "\n\nfrom: " + name + "\n" + from_email, 
                      'thedofusfashionista@gmail.com', 
                      ['thedofusfashionista@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect(reverse('chardata.contact_view.thankyou'))
    else:
        return HttpResponseRedirect(reverse('chardata.contact_view.nomessage'))
        
def thankyou(request):
    return set_response(request,
                        'chardata/thankyou.html',
                        {})
def nomessage(request):
    return set_response(request,
                        'chardata/nomessage.html',
                        {})
