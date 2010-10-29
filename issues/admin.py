from models import *
from django.contrib import admin





class DetailInline(admin.StackedInline):
    model = Detail
    extra = 0

class IssueAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','checked', 'date_of_problem','date_of_decision','title', 'url_of_complaint' )
    list_display_links = ('checked', 'title' )

    list_filter = [ 'checked', 'clauses','tags', 'complaining_about']
    search_fields = ['title','description']
    raw_id_fields = ('related', )
    inlines = [DetailInline,]

admin.site.register(Entity)
admin.site.register(Issue,IssueAdmin)
admin.site.register(Tag)
admin.site.register(Clause)
#admin.site.register(Detail)
admin.site.register(Outcome)

