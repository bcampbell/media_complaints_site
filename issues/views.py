# Create your views here.
from django.http import HttpResponse,Http404
from django.template import Context, loader
from models import *
from django.shortcuts import render_to_response

def issue_detail(request, issue_id):
    try:
        issue = Issue.objects.get(pk=issue_id)
    except Issue.DoesNotExist:
        raise Http404
    return render_to_response('issue.html', {'issue': issue})


def keyword(request, kw):
    try:
        obj = Keyword.objects.get(name=kw)
    except Keyword.DoesNotExist:
        raise Http404
    return render_to_response('keyword.html', {'kw': obj})

def complaint_code(request, clause ):
    try:
        obj = ComplaintCode.objects.get(clause=clause)
    except Keyword.DoesNotExist:
        raise Http404
    return render_to_response('code.html', {'code': obj})

