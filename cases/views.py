# Create your views here.
from django.http import HttpResponse,Http404
from django.template import Context, loader
from django.template import RequestContext

from models import *
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.db.models import Count

def entity_detail(request, object_id):
    try:
        obj = Entity.objects.get(pk=object_id)
    except Entity.DoesNotExist:
        raise Http404

    clause_stats = Clause.objects.filter( case__defendants__in=(obj,) ).distinct().annotate( num_cases=Count( 'case' ) )
    return render_to_response('entity_detail.html', {'ent': obj,'clause_stats': clause_stats })


def tag_detail(request, tag):
    try:
        obj = Tag.objects.get(name=tag)
    except Keyword.DoesNotExist:
        raise Http404
    return render_to_response('tag_detail.html', {'tag': obj})


def clause_detail(request, clause_id ):
    try:
        obj = Clause.objects.get(pk=clause_id)
    except Keyword.DoesNotExist:
        raise Http404
    return render_to_response('clause_detail.html', {'clause': obj})

