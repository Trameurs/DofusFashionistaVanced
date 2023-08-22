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

from django.urls import include, re_path
from django.views.i18n import JavaScriptCatalog
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import TemplateView
from chardata import home_view, login_view, views, projects_view, base_stats_view, create_project_view, \
    stats_weights_view, min_stats_view, options_view, inclusions_view, exclusions_view, wizard_view, \
    fashion_action, solution_view, spells_view, contact_view, manage_account_view, util, manage_items_view, \
    compare_sets_view, item_exchange, util_views
admin.autodiscover()

js_info_dict = {
    'packages': 'chardata',
}

urlpatterns = [
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog', kwargs=js_info_dict),
    re_path(r'^$', home_view.home, name='home'),
    re_path(r'^login_page/', login_view.login_page, name='login_page'),
    re_path(r'^local_login/', login_view.local_login),
    re_path(r'^register/', login_view.register, name='register'),
    re_path(r'^check_your_email/', login_view.check_your_email),
    re_path(r'^confirm_email/(?P<username>.+)/(?P<confirmation_token>.+)/', login_view.confirm_email, name='confirm_email'),
    re_path(r'^check_username/', login_view.check_if_taken),
    re_path(r'^change_password/', login_view.change_password),
    re_path(r'^email_confirmed/(?P<username>.+)/(?P<already_confirmed>.+)/', login_view.email_confirmed_page),
    re_path(r'^recover_password/', login_view.recover_password_page),
    re_path(r'^recover_password_from_register/(?P<email>.+)/', login_view.recover_password_page_from_register),
    re_path(r'^do_recover_password/(?P<username>.+)/(?P<recover_token>.+)/', login_view.recover_password),
    re_path(r'^recover_password_email/', login_view.recover_password_email_page, name='recover_password_email_page'),

    re_path(r'^loadprojects/', views.load_projects, name='load_projects'),
    re_path(r'^loadprojectserror/(?P<error>.+)/', views.load_projects_error),
    re_path(r'^loadproject/(?P<char_id>\d+)/', views.load_a_project),
    re_path(r'^deleteprojects/', projects_view.delete_projects),
    re_path(r'^duplicateproject/', projects_view.duplicate_project),
    re_path(r'^duplicatemyproject/(?P<char_id>\d+)/', projects_view.duplicate_my_project),
    re_path(r'^duplicatesomeonesproject/(?P<encoded_char_id>.+)/', projects_view.duplicate_someones_project),

    re_path(r'^setup/(?P<char_id>\d+)/', base_stats_view.setup_base_stats),
    re_path(r'^save_char/(?P<char_id>\d+)/', base_stats_view.save_char),
    re_path(r'^initbasestats/(?P<char_id>\d+)/', base_stats_view.init_base_stats),
    re_path(r'^initbasestatspost/(?P<char_id>\d+)/', base_stats_view.init_base_stats_post),

    re_path(r'^setup/$', create_project_view.setup, name='setup'),
    re_path(r'^createproject/', create_project_view.create_project, name='create_project'),
    re_path(r'^saveprojecttouser/', create_project_view.save_project_to_user, name='save_project_to_user'),
    re_path(r'^project/(?P<char_id>\d+)/', create_project_view.setup),
    re_path(r'^saveproject/(?P<char_id>\d+)/', create_project_view.save_project_to_user),
    re_path(r'^project/(?P<char_id>\d+)/', create_project_view.setup),
    re_path(r'^saveproject/(?P<char_id>\d+)/', create_project_view.save_project, name='save_project'),
    re_path(r'^understandbuild/', create_project_view.understand_build_post),

    re_path(r'^stats/(?P<char_id>\d+)/', stats_weights_view.stats),
    re_path(r'^statspost/(?P<char_id>\d+)/', stats_weights_view.stats_post),

    re_path(r'^min_stats/(?P<char_id>\d+)/', min_stats_view.min_stats),
    re_path(r'^minstatspost/(?P<char_id>\d+)/', min_stats_view.min_stats_post),

    re_path(r'^options/(?P<char_id>\d+)/', options_view.options),
    re_path(r'^optionspost/(?P<char_id>\d+)/', options_view.options_post),

    re_path(r'^inclusions/(?P<char_id>\d+)/', inclusions_view.inclusions),
    re_path(r'^inclusionspost/(?P<char_id>\d+)/', inclusions_view.inclusions_post),
    re_path(r'^getitemdetails/', inclusions_view.get_item_details),

    re_path(r'^exclusions/(?P<char_id>\d+)/', exclusions_view.exclusions),
    re_path(r'^exclusionspost/(?P<char_id>\d+)/', exclusions_view.exclusions_post),

    re_path(r'^wizard/(?P<char_id>\d+)/', wizard_view.wizard, name='wizard'),
    re_path(r'^wizardpost/(?P<char_id>\d+)/', wizard_view.wizard_post),
    re_path(r'^wizardgetsliders/(?P<char_id>\d+)/', wizard_view.get_resetted_sliders),

    re_path(r'^fashion/(?P<char_id>\d+)/', fashion_action.fashion),

    re_path(r'^solution/(?P<char_id>\d+)/(?P<empty>.*)/', solution_view.solution, name='solution'),
    re_path(r'^solution/(?P<char_id>\d+)/', solution_view.solution),
    re_path(r'^getsharinglink/(?P<char_id>\d+)/', solution_view.get_sharing_link),
    re_path(r'^hidesharinglink/(?P<char_id>\d+)/', solution_view.hide_sharing_link),
    re_path(r'^s/(?P<char_name>.*)/(?P<encoded_char_id>.+)/', solution_view.solution_linked),
    re_path(r'^setitemlocked/(?P<char_id>\d+)/', solution_view.set_item_locked),
    re_path(r'^setitemforbidden/(?P<char_id>\d+)/', solution_view.set_item_forbidden),
    re_path(r'^itemexchange/(?P<char_id>\d+)/', item_exchange.get_items_to_exchange),
    re_path(r'^itemadd/(?P<char_id>\d+)/', item_exchange.get_items_of_type),
    re_path(r'^exchange/(?P<char_id>\d+)/', item_exchange.switch_item),
    re_path(r'^remove/(?P<char_id>\d+)/', item_exchange.remove_item),

    re_path(r'^infeasible/(?P<char_id>\d+)/', views.infeasible),
    re_path(r'^error/(?P<char_id>\d+)/', util_views.error),
    re_path(r'^about/', views.about, name='about'),
    re_path(r'^license/', views.license_page, name='license_page'),
    re_path(r'^faq/', views.faq, name='faq'),

    re_path(r'^spells/(?P<char_id>\d+)/', spells_view.spells),
    re_path(r'^spells_linked/(?P<char_name>.*)/(?P<encoded_char_id>.+)/', spells_view.spells_linked),

    re_path(r'^403/', views.forbidden),
    re_path(r'^404/', views.not_found),
    re_path(r'^500/', views.app_error),

    re_path(r'^contact/thankyou/', contact_view.thankyou),
    re_path(r'^contact/', contact_view.contact, name = 'contact'),
    re_path(r'^send/', contact_view.send_email),

    re_path(r'^manageaccount/', manage_account_view.manage_account),
    re_path(r'^saveaccount/', manage_account_view.save_account),
    
    re_path(r'^changetheme/', util.set_theme),
    re_path(r'^changeautotheme/', util.set_current_auto),

    re_path('', include('social_django.urls', namespace='social')),
    re_path('', include(('django.contrib.auth.urls', 'auth'))),

    re_path(r'^robots\.txt$', TemplateView.as_view(template_name='chardata/robots.txt',
                                               content_type='text/plain')),
                                               
                                               
    
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^edit_item/$', manage_items_view.edit_item),
        re_path(r'^edit_item/(?P<item_id>\d+)/', manage_items_view.edit_item),
        re_path(r'^edit_item_search_item/', manage_items_view.edit_item_search_item),
        re_path(r'^choose_item/', manage_items_view.choose_item),
        re_path(r'^update_item/', manage_items_view.update_item_post),
        re_path(r'^delete_item/', manage_items_view.delete_item_post),
        re_path(r'^edit_item_search_sets/', manage_items_view.edit_item_search_sets),
        re_path(r'^edit_set/', manage_items_view.edit_set),
        re_path(r'^choose_set/', manage_items_view.choose_set),
        re_path(r'^update_set/', manage_items_view.update_set_post),
        re_path(r'^delete_set/', manage_items_view.delete_set_post),
        re_path(r'^admin/', admin.site.urls),
    ]

if settings.EXPERIMENTS['COMPARE_SETS']:
    urlpatterns += [
                            re_path(r'^compare_sets/(?P<sets_params>.+)', compare_sets_view.compare_sets),
                            re_path(r'^choose_compare_sets/$', compare_sets_view.choose_compare_sets, name = 'choose_compare_sets'),
                            re_path(r'^choose_compare_sets_post/$', compare_sets_view.choose_compare_sets_post),
                            re_path(r'^get_compare_sharing_link/(?P<sets_params>.+)', compare_sets_view.get_sharing_link),
                            re_path(r'^get_item_stats_compare/$', compare_sets_view.get_item_stats),
                            re_path(r'^compare_set_search_proj_name/$', compare_sets_view.compare_set_search_proj_name),]

if settings.EXPERIMENTS['TRANSLATION']:
    urlpatterns += [
                            re_path(r'^i18n/', include('django.conf.urls.i18n'))]

urlpatterns += staticfiles_urlpatterns()
handler403 = views.forbidden
handler404 = views.not_found
handler500 = views.app_error
