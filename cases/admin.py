from models import *
from django.contrib import admin,messages

#merge stuff
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.template import RequestContext
from helpers import merge_model_objects


from filterspecs import YearFilterSpec


class DetailInline(admin.StackedInline):
    model = Detail
    extra = 0


class CaseAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','title','date_of_decision', 'url_of_complaint','offending_page','correction_info','checked' )
    list_display_links = ('id','title' )

    list_filter = [ 'date_of_decision', 'judgement','complainant_type', 'checked', 'clauses','tags' ]
    search_fields = ['title','complaint','summary']
    inlines = [DetailInline,]
    filter_horizontal = ['offending_articles','related_cases','related_links','complainants','defendants','clauses','related_cases','tags']

    def correction_info(self,obj):
        """ show info about correction, if any """

        # might not have the data
        if obj.correction_page is None:
            return ''
        if obj.offending_page is None:
            return str(obj.correction_page)

        return "%d (%+d)" % (obj.correction_page, obj.correction_page - obj.offending_page)
    correction_info.short_description = "correction page"


class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ['authors',]




class EntityAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','kind','publication_type','num_uses' )
    list_display_links = ('id','name' )
    list_filter = [ 'kind','publication_type' ]
    search_fields = ['name',]
    actions = ['merge_entities', 'set_uklocal', 'set_uknational', 'set_ukmag']

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


    def set_uklocal(modeladmin,request,queryset):
        queryset.update(publication_type='uklocal')
    def set_uknational(modeladmin,request,queryset):
        queryset.update(publication_type='uknational')
    def set_ukmag(modeladmin,request,queryset):
        queryset.update(publication_type='ukmag')


admin.site.register(Entity,EntityAdmin)
admin.site.register(Case,CaseAdmin)
admin.site.register(Tag)
admin.site.register(Clause)
#admin.site.register(Detail)
admin.site.register(Outcome)
admin.site.register(Article,ArticleAdmin)

