from models import *
from django.contrib import admin





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
    list_display = ('id','name','kind' )
    list_display_links = ('id','name' )
    list_filter = [ 'kind', ]
    search_fields = ['name',]

admin.site.register(Entity,EntityAdmin)
admin.site.register(Case,CaseAdmin)
admin.site.register(Tag)
admin.site.register(Clause)
#admin.site.register(Detail)
admin.site.register(Outcome)
admin.site.register(Article,ArticleAdmin)

