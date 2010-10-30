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
    url(r'^tag/(?P<tag>[\sa-zA-Z]+)/$', 'issues.views.tag_detail', name='tag-detail'),
    url(r'^clause/(?P<clause_id>[\s0-9a-zA-Z]+)/$', 'issues.views.clause_detail', name='clause-detail'),
    url(r'^ent/(?P<entity_id>[\s0-9a-zA-Z]+)/$', 'issues.views.entity_detail', name='entity-detail'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
