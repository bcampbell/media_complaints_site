from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^media_complaints_site/', include('media_complaints_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'cases.views.case_list', name='case-list'),
    url(r'^case/(?P<case_id>\d+)/$', 'cases.views.case_detail', name='case-detail'),
    url(r'^tag/(?P<tag>[\sa-zA-Z]+)/$', 'cases.views.tag_detail', name='tag-detail'),
    url(r'^clause/(?P<clause_id>[\s0-9a-zA-Z]+)/$', 'cases.views.clause_detail', name='clause-detail'),
    url(r'^ent/(?P<entity_id>[\s0-9a-zA-Z]+)/$', 'cases.views.entity_detail', name='entity-detail'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

