from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'account.views.home', name='account_home'),
    url(r'^login/$', 'account.views.login', name='account_login'),
    url(r'^logout/$', 'account.views.logout', name='account_logout'),
    url(r'^dropbox-logout/$', 'account.views.dropbox_logout', name='dropbox_logout'),
     url(r'^dropbox-auth-start/$', 'account.views.dropbox_auth_start', name='dropbox_auth_start'),
     url(r'^dropbox-auth-finish/$', 'account.views.dropbox_auth_finish', name='dropbox_auth_finish'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
