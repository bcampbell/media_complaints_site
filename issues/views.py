# Create your views here.
from django.http import HttpResponse,Http404
from django.template import Context, loader
from models import *
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage



def issue_list(request):
    paginator = Paginator(Issue.objects.all(), 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        issues = paginator.page(page)
    except (EmptyPage, InvalidPage):
        issues = paginator.page(paginator.num_pages)

    return render_to_response('issue_list.html', {"issues": issues})


def issue_detail(request, issue_id):
    try:
        obj = Issue.objects.get(pk=issue_id)
    except Issue.DoesNotExist:
        raise Http404
    return render_to_response('issue_detail.html', {'issue': obj})


def entity_detail(request, entity_id):
    try:
        obj = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404
    return render_to_response('entity_detail.html', {'ent': obj})


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

