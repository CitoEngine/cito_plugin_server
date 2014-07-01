"""Copyright 2014 Cyrus Dasadia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/(?P<apikey>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/runplugin',
                           'webservice.api.run_plugin'),
                       url(r'^api/(?P<apikey>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/getallplugins',
                           'webservice.api.get_all_plugins'),
                       )

urlpatterns += patterns('',
                        url(r'^$', 'webservice.views.auth_views.login_user'),
                        url(r'^login/$', 'webservice.views.auth_views.login_user'),
                        url(r'^logout/$', 'webservice.views.auth_views.logout_user'),
                        )

urlpatterns += patterns('',
                        url(r'^plugins/$', 'webservice.views.plugin_views.view_all_plugins'),
                        url(r'^plugins/add/$', 'webservice.views.plugin_views.add_new_plugin'),
                        url(r'^plugins/edit/(?P<plugin_id>\d+)/$', 'webservice.views.plugin_views.edit_plugin'),
                        )

urlpatterns += patterns('',
                        url(r'^apikeys/$', 'webservice.views.apikey_views.view_all_apikeys'),
                        url(r'^apikeys/add/$', 'webservice.views.apikey_views.add_new_key'),
                        url(r'^apikeys/edit/(?P<apikey_id>\d+)/$', 'webservice.views.apikey_views.edit_key'),
                        )

urlpatterns += patterns('',
                        url(r'^users/$', 'webservice.views.user_views.view_all_users'),
                        url(r'^users/create/$', 'webservice.views.user_views.create_user'),
                        url(r'^users/edit/(?P<user_id>\d+)/$', 'webservice.views.user_views.edit_user'),
                        url(r'^users/toggle/$', 'webservice.views.user_views.toggle_user'),
                        url(r'^users/view/(?P<user_id>\d+)/$', 'webservice.views.user_views.view_single_user'),
                        )

urlpatterns += patterns('',
                        url(r'^content/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.STATIC_FILES}),)

