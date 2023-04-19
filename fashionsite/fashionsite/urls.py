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

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

js_info_dict = {
    'packages': ('fashionsite',),
}

urlpatterns = patterns('',
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)


urlpatterns = patterns('',
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^$', 'chardata.home_view.home', name='home'),
    url(r'^login_page/', 'chardata.login_view.login_page'),
    url(r'^local_login/', 'chardata.login_view.local_login'),
    url(r'^register/', 'chardata.login_view.register'),
    url(r'^check_your_email/', 'chardata.login_view.check_your_email'),
    url(r'^confirm_email/(?P<username>.+)/(?P<confirmation_token>.+)/',
        'chardata.login_view.confirm_email'),
    url(r'^check_username/', 'chardata.login_view.check_if_taken'),
    url(r'^change_password/', 'chardata.login_view.change_password'),
    url(r'^email_confirmed/(?P<username>.+)/(?P<already_confirmed>.+)/',
        'chardata.login_view.email_confirmed_page'),
    url(r'^recover_password/', 'chardata.login_view.recover_password_page'),
    url(r'^recover_password_from_register/(?P<email>.+)/',
        'chardata.login_view.recover_password_page_from_register'),
    url(r'^do_recover_password/(?P<username>.+)/(?P<recover_token>.+)/',
        'chardata.login_view.recover_password'),
    url(r'^recover_password_email/', 'chardata.login_view.recover_password_email_page'),

    url(r'^loadprojects/', 'chardata.views.load_projects'),
    url(r'^loadprojectserror/(?P<error>.+)/', 'chardata.views.load_projects_error'),
    url(r'^loadproject/(?P<char_id>\d+)/', 'chardata.views.load_a_project'),
    url(r'^deleteprojects/', 'chardata.projects_view.delete_projects'),
    url(r'^duplicateproject/', 'chardata.projects_view.duplicate_project'),
    url(r'^duplicatemyproject/(?P<char_id>\d+)/',
        'chardata.projects_view.duplicate_my_project'),
    url(r'^duplicatesomeonesproject/(?P<encoded_char_id>.+)/',
        'chardata.projects_view.duplicate_someones_project'),

    url(r'^setup/(?P<char_id>\d+)/', 'chardata.base_stats_view.setup_base_stats'),
    url(r'^save_char/(?P<char_id>\d+)/', 'chardata.base_stats_view.save_char'),
    url(r'^initbasestats/(?P<char_id>\d+)/', 'chardata.base_stats_view.init_base_stats'),
    url(r'^initbasestatspost/(?P<char_id>\d+)/', 'chardata.base_stats_view.init_base_stats_post'),

    url(r'^setup/$', 'chardata.create_project_view.setup'),
    url(r'^createproject/', 'chardata.create_project_view.create_project'),
    url(r'^saveprojecttouser/', 'chardata.create_project_view.save_project_to_user'),
    url(r'^project/(?P<char_id>\d+)/', 'chardata.create_project_view.setup'),
    url(r'^saveproject/(?P<char_id>\d+)/', 'chardata.create_project_view.save_project'),
    url(r'^understandbuild/', 'chardata.create_project_view.understand_build_post'),

    url(r'^stats/(?P<char_id>\d+)/', 'chardata.stats_weights_view.stats'),
    url(r'^statspost/(?P<char_id>\d+)/', 'chardata.stats_weights_view.stats_post'),

    url(r'^min_stats/(?P<char_id>\d+)/', 'chardata.min_stats_view.min_stats'),
    url(r'^minstatspost/(?P<char_id>\d+)/', 'chardata.min_stats_view.min_stats_post'),

    url(r'^options/(?P<char_id>\d+)/', 'chardata.options_view.options'),
    url(r'^optionspost/(?P<char_id>\d+)/', 'chardata.options_view.options_post'),

    url(r'^inclusions/(?P<char_id>\d+)/', 'chardata.inclusions_view.inclusions'),
    url(r'^inclusionspost/(?P<char_id>\d+)/', 'chardata.inclusions_view.inclusions_post'),
    url(r'^getitemdetails/', 'chardata.inclusions_view.get_item_details'),

    url(r'^exclusions/(?P<char_id>\d+)/', 'chardata.exclusions_view.exclusions'),
    url(r'^exclusionspost/(?P<char_id>\d+)/', 'chardata.exclusions_view.exclusions_post'),

    url(r'^wizard/(?P<char_id>\d+)/', 'chardata.wizard_view.wizard'),
    url(r'^wizardpost/(?P<char_id>\d+)/', 'chardata.wizard_view.wizard_post'),
    url(r'^wizardgetsliders/(?P<char_id>\d+)/', 'chardata.wizard_view.get_resetted_sliders'),

    url(r'^fashion/(?P<char_id>\d+)/', 'chardata.fashion_action.fashion'),

    url(r'^solution/(?P<char_id>\d+)/(?P<empty>.*)/', 'chardata.solution_view.solution'),
    url(r'^solution/(?P<char_id>\d+)/', 'chardata.solution_view.solution'),
    url(r'^getsharinglink/(?P<char_id>\d+)/', 'chardata.solution_view.get_sharing_link'),
    url(r'^hidesharinglink/(?P<char_id>\d+)/', 'chardata.solution_view.hide_sharing_link'),
    url(r'^s/(?P<char_name>.*)/(?P<encoded_char_id>.+)/', 'chardata.solution_view.solution_linked'),
    url(r'^setitemlocked/(?P<char_id>\d+)/', 'chardata.solution_view.set_item_locked'),
    url(r'^setitemforbidden/(?P<char_id>\d+)/', 'chardata.solution_view.set_item_forbidden'),
    url(r'^itemexchange/(?P<char_id>\d+)/', 'chardata.item_exchange.get_items_to_exchange'),
    url(r'^itemadd/(?P<char_id>\d+)/', 'chardata.item_exchange.get_items_of_type'),
    url(r'^exchange/(?P<char_id>\d+)/', 'chardata.item_exchange.switch_item'),
    url(r'^remove/(?P<char_id>\d+)/', 'chardata.item_exchange.remove_item'),

    url(r'^infeasible/(?P<char_id>\d+)/', 'chardata.views.infeasible'),
    url(r'^error/(?P<char_id>\d+)/', 'chardata.util_views.error'),
    url(r'^about/', 'chardata.views.about'),
    url(r'^license/', 'chardata.views.license_page'),
    url(r'^faq/', 'chardata.views.faq'),

    url(r'^spells/(?P<char_id>\d+)/', 'chardata.spells_view.spells'),
    url(r'^spells_linked/(?P<char_name>.*)/(?P<encoded_char_id>.+)/', 'chardata.spells_view.spells_linked'),

    url(r'^403/', 'chardata.views.forbidden'),
    url(r'^404/', 'chardata.views.not_found'),
    url(r'^500/', 'chardata.views.app_error'),

    url(r'^contact/thankyou/', 'chardata.contact_view.thankyou'),
    url(r'^contact/', 'chardata.contact_view.contact'),
    url(r'^send/', 'chardata.contact_view.send_email'),

    url(r'^manageaccount/', 'chardata.manage_account_view.manage_account'),
    url(r'^saveaccount/', 'chardata.manage_account_view.save_account'),
    
    url(r'^changetheme/', 'chardata.util.set_theme'),
    url(r'^changeautotheme/', 'chardata.util.set_current_auto'),

    url('', include('social_django.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='chardata/robots.txt',
                                               content_type='text/plain')),
                                               
                                               
    
)

if settings.DEBUG:
    urlpatterns += patterns('chardata.manage_items_view',
                            url(r'^edit_item/$', 'edit_item'),
                            url(r'^edit_item/(?P<item_id>\d+)/', 'edit_item'),
                            url(r'^edit_item_search_item/', 'edit_item_search_item'),
                            url(r'^choose_item/', 'choose_item'),
                            url(r'^update_item/', 'update_item_post'),
                            url(r'^delete_item/', 'delete_item_post'),
                            url(r'^edit_item_search_sets/', 'edit_item_search_sets'),
                            url(r'^edit_set/', 'edit_set'),
                            url(r'^choose_set/', 'choose_set'),
                            url(r'^update_set/', 'update_set_post'),
                            url(r'^delete_set/', 'delete_set_post'),)
    urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))

if settings.EXPERIMENTS['COMPARE_SETS']:
    urlpatterns += patterns('',
                            url(r'^compare_sets/(?P<sets_params>.+)', 'chardata.compare_sets_view.compare_sets'),
                            url(r'^choose_compare_sets/$', 'chardata.compare_sets_view.choose_compare_sets'),
                            url(r'^choose_compare_sets_post/$', 'chardata.compare_sets_view.choose_compare_sets_post'),
                            url(r'^get_compare_sharing_link/(?P<sets_params>.+)', 'chardata.compare_sets_view.get_sharing_link'),
                            url(r'^get_item_stats_compare/$', 'chardata.compare_sets_view.get_item_stats'),
                            url(r'^compare_set_search_proj_name/$', 'chardata.compare_sets_view.compare_set_search_proj_name'),)

if settings.EXPERIMENTS['TRANSLATION']:
    urlpatterns += patterns('',
                            url(r'^i18n/', include('django.conf.urls.i18n')))

urlpatterns += staticfiles_urlpatterns()
handler403 = 'chardata.views.forbidden'
handler404 = 'chardata.views.not_found'
handler500 = 'chardata.views.app_error'
