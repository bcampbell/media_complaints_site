import csv
from django.http import HttpResponse,Http404
from django.template import Context, loader
from django.template import RequestContext

from models import *
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required


from django.db.models import Count

def entity_detail(request, object_id):
    try:
        obj = Entity.objects.get(pk=object_id)
    except Entity.DoesNotExist:
        raise Http404

    clause_stats = Clause.objects.filter( parent=None,case__defendants__in=(obj,) ).distinct().annotate( num_cases=Count( 'case' ) )
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



from helpers import get_query





def search(request):
    query_string = ''
    found = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['title', 'summary', 'complaint', 'defendants__name', 'complainants__name', 'detail__content'])

        found = Case.objects.filter(entry_query)    #.order_by('-date_of_decision')
    else:
        query_string = ''
        found = Case.objects.all()


    class Refiner:
        def __init__(self, label,value ):
            self.label=label
            self.value=value

    # refine by date
    date_refiner_list = [ Refiner( 'All','all') ]
    years = range(1996,2012)    # TODO: get max year from DB!
    years.reverse()
    for year in years:
        date_refiner_list.append( Refiner( str(year), str(year) ) )

    date_refine = 'all'
    if ('date' in request.GET) and request.GET['date'].strip():
        date_refine = request.GET['date'].strip()


    if date_refine != 'all':
        found = found.filter( date_of_decision__year=int(date_refine) )


    # refine by issue
    issue_refiner_list = [ Refiner( c.prettyname,str(c.id) ) for c in Clause.objects.filter(parent=None).order_by( 'id' ) ]
    issue_refiner_list.insert(0, Refiner( 'All','all') )
    issue_refine = 'all'
    if ('issue' in request.GET) and request.GET['issue'].strip():
        issue_refine = request.GET['issue'].strip()
    if issue_refine != 'all':
#        c = Clause.objects.get( pk=int(issue_refine) )
        found = found.filter( clauses__id=issue_refine )

    # refine by outcome
    outcome_refiner_list = [ Refiner( o.name,str(o.id) ) for o in Outcome.objects.all().order_by( 'name' ) ]
    outcome_refiner_list.insert(0, Refiner( 'All','all') )
    outcome_refine = 'all'
    if ('outcome' in request.GET) and request.GET['outcome'].strip():
        outcome_refine = request.GET['outcome'].strip()
    if outcome_refine != 'all':
        found = found.filter( outcome__id=outcome_refine )

    return render_to_response('search.html',
                          { 'query_string': query_string,
                            'case_list': found,
                            'date_refine': date_refine,
                            'date_refiner_list': date_refiner_list,
                            'issue_refine': issue_refine,
                            'issue_refiner_list': issue_refiner_list,
                            'outcome_refine': outcome_refine,
                            'outcome_refiner_list': outcome_refiner_list,
                          },
                          context_instance=RequestContext(request))


def front_page(request):
    context = {}
    context['top_defendants'] = Entity.objects.all().annotate( num_cases=Count('cases_as_defendant') ).order_by('-num_cases')[:10]
    context['top_complainants'] = Entity.objects.all().annotate( num_cases=Count('cases_as_complainant') ).order_by('-num_cases')[:10]
    context['top_tags'] = Tag.objects.all().annotate( num_cases=Count('case') ).order_by('-num_cases')[:10]
    context['top_issues'] = Clause.objects.filter(parent=None).annotate( num_cases=Count('case') ).order_by('-num_cases')

    #celeb = Tag.objects.get( name='Celebrity' )
    #context['notable_case_list'] = Case.objects.filter( tags__in=[celeb] )
    model_cases = (396,574,59,774,170)
    context['notable_case_list'] = Case.objects.filter( pk__in=model_cases )

    return render_to_response('front_page.html', context)





def dump(request):
    """ dump out csv file of case data """
    # check for admin
    if not request.user.is_staff:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res

    found = Case.objects.all()

    year = 'all'
    if ('year' in request.GET) and request.GET['year'].strip():
        year = request.GET['year'].strip()
    if year != 'all':
        found = found.filter( date_of_decision__year=int(year) )

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pccdump_%s.csv' % (year)

    writer = csv.writer(response)

    fieldnames = ('Title',
        'Complainant',
        'Defendant',
        'Clauses',
        'Complainant type',
        'Judgement',
        'Offending page',
        'Offending date',
        'Date of decision',
        'Chosen tags',
        'Kind')
    writer.writerow(fieldnames)

    for case in found:
        kind = ''
        detail = case.detail_set.all()[0]
        kind = detail.kind

        row = [case.title,
            ','.join([unicode(e) for e in case.complainants.all()]),
            ','.join([unicode(e) for e in case.defendants.all()]),
            ','.join([unicode(e) for e in case.clauses.all()]),
            case.complainant_type,
            case.judgement,
            case.offending_page,
            case.offending_date,
            case.date_of_decision,
            ','.join([unicode(t) for t in case.tags.all()]),
            kind]
        row = [unicode(s).encode('utf-8') for s in row]
        writer.writerow(row)
    return response

