from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^media_complaints_site/', include('media_complaints_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^issue/(?P<issue_id>\d+)/$', 'issues.views.issue_detail', name='issue-detail'),
    url(r'^keyword/(?P<kw>[\sa-zA-Z]+)/$', 'issues.views.keyword', name='keyword'),
    url(r'^code/(?P<clause>[\s0-9a-zA-Z]+)/$', 'issues.views.complaint_code', name='clause'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
