from models import *
from django.contrib import admin


class IssueAdmin(admin.ModelAdmin):
    # ...
    list_display = ('checked', 'title' )
    list_display_links = ('checked', 'title' )

    list_filter = [ 'checked', 'codes' ]
    search_fields = ['title','description']

admin.site.register(Entity)
admin.site.register(Issue,IssueAdmin)
admin.site.register(Tag)
admin.site.register(ComplaintCode)

