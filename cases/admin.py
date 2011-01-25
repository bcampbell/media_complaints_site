from models import *
from django.contrib import admin,messages

#merge stuff
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.template import RequestContext
from helpers import merge_model_objects




class DetailInline(admin.StackedInline):
    model = Detail
    extra = 0


class CaseAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','title','date_of_complaint','date_of_decision', 'url_of_complaint','checked' )
    list_display_links = ('id','title' )

    list_filter = [ 'checked', 'clauses','tags', 'defendants']
    search_fields = ['title','description','summary']
#    raw_id_fields = ('related_cases', )
    inlines = [DetailInline,]
    filter_horizontal = ['offending_articles','related_cases','related_links','complainants','defendants','clauses','related_cases','tags']

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ['authors',]




class EntityAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','kind','num_uses' )
    list_display_links = ('id','name' )
    list_filter = [ 'kind', ]
    search_fields = ['name',]
    actions = [ 'merge_entities' ]

    def merge_entities(modeladmin,request,queryset):
        if queryset.count() < 2:
            messages.error( request, "Need to select 2 or more to merge" )
            return

        return_url = "."
        ids = []
        if '_selected_action' in request.POST: #List of PK's of the selected models
            ids = request.POST.getlist('_selected_action')

        if 'master' in request.POST:
            model= Entity
            master = model.objects.get(id=request.POST['master'])
            queryset = model.objects.filter(pk__in=ids)
            for obj in queryset.exclude(pk=master.pk):
                merge_model_objects(master,obj)
            messages.success(request, "Entities merged into %s (id=%d)" % (master.name, master.id))
            return

        # show the intermediate page to pick target
        return render_to_response('admin/merge_entity_preview.html',{'entity_list': queryset, 'return_url':return_url, 'ids': ids}, context_instance=RequestContext(request))

    merge_entities.short_description = "Merge selected entities"




admin.site.register(Entity,EntityAdmin)
admin.site.register(Case,CaseAdmin)
admin.site.register(Tag)
admin.site.register(Clause)
#admin.site.register(Detail)
admin.site.register(Outcome)
admin.site.register(Article,ArticleAdmin)

