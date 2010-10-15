from models import *
from django.contrib import admin


class IssueAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','checked', 'date_of_problem','date_of_decision','title','outcome_keyword' )
    list_display_links = ('checked', 'title' )

    list_filter = [ 'checked', 'codes','keywords', 'outcome_keyword', 'about']
    search_fields = ['title','description']
    raw_id_fields = ('related', )

admin.site.register(Entity)
admin.site.register(Issue,IssueAdmin)
admin.site.register(Keyword)
admin.site.register(ComplaintCode)

