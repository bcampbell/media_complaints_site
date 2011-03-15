from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic import list_detail,simple

from media_complaints_site.cases.models import *

admin.autodiscover()

case_dict = { 'queryset': Case.objects.all(), }
clause_dict = { 'queryset': Clause.objects.filter(parent=None), }
tag_dict = { 'queryset': Tag.objects.all(), }

urlpatterns = patterns('',
    # Example:
    # (r'^media_complaints_site/', include('media_complaints_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

#    url(r'^$', 'cases.views.case_list', name='case-list'),
    url( r'^$', 'cases.views.front_page', name='front-page', ),

    # cases
    url( r'^cases$', list_detail.object_list,
            dict( case_dict,
                template_name='case_list.html',
                template_object_name="case" ),
            name='case-list',
            ),
    url(r'^case/(?P<object_id>\d+)/$', list_detail.object_detail,
            dict( case_dict,
                template_name='case_detail.html',
                template_object_name="case" ),
            name='case-detail'),

    #
    url( r'complainants$', list_detail.object_list,
            dict( {'queryset': Entity.objects.filter( cases_as_complainant__in=Case.objects.all() ).distinct() },
                template_name='complainant_list.html',
                template_object_name="complainant" ),
            name='complainant-list',
            ),

    #
    url( r'defendants$', list_detail.object_list,
            dict( {'queryset': Entity.objects.filter( cases_as_defendant__in=Case.objects.all() ).distinct() },
                template_name='defendant_list.html',
                template_object_name="defendant" ),
            name='defendant-list',
            ),

    #
#    url(r'^entity/(?P<object_id>\d+)/$', list_detail.object_detail,
#            dict( {'queryset': Entity.objects.all() },
#                template_name='entity_detail.html',
#                template_object_name="ent" ),
#            name='entity-detail'),
    url(r'^entity/(?P<object_id>[\s0-9a-zA-Z]+)/$', 'cases.views.entity_detail', name='entity-detail'),

    # clauses
    url( r'clauses$', list_detail.object_list,
            dict( clause_dict,
                template_name='clause_list.html',
                template_object_name="clause" ),
            name='clause-list',
            ),
    url(r'^clause/(?P<object_id>\d+)/$', list_detail.object_detail,
            dict( clause_dict,
                template_name='clause_detail.html',
                template_object_name="clause" ),
            name='clause-detail'),

    # tags
    url( r'tags$', list_detail.object_list,
            dict( tag_dict,
                template_name='tag_list.html',
                template_object_name="tag" ),
            name='tag-list',
            ),
    url(r'^tag/(?P<object_id>\d+)/$', list_detail.object_detail,
            dict( tag_dict,
                template_name='tag_detail.html',
                template_object_name="tag" ),
            name='tag-detail'),

#    url(r'^case/(?P<case_id>\d+)/$', 'cases.views.case_detail', name='case-detail'),
#    url(r'^tag/(?P<tag>[\sa-zA-Z]+)/$', 'cases.views.tag_detail', name='tag-detail'),
#    url(r'^clause/(?P<clause_id>[\s0-9a-zA-Z]+)/$', 'cases.views.clause_detail', name='clause-detail'),
#    url(r'^ent/(?P<entity_id>[\s0-9a-zA-Z]+)/$', 'cases.views.entity_detail', name='entity-detail'),
    url(r'^article$', list_detail.object_list,
            dict( { 'queryset': Article.objects.all(), },
            template_name='article_list.html',
            template_object_name="article"
            ), ),
    url(r'^search$', 'cases.views.search', name='search'),
    url(r'^about/$', simple.direct_to_template, { 'template': 'about.html' } ),
    url(r'^dump$', 'cases.views.dump', name='dump'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

