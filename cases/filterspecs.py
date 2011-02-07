from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, DateFieldFilterSpec
from django.utils.translation import ugettext as _
from datetime import datetime

class YearFilterSpec(DateFieldFilterSpec):
    """
    Adds filtering by year in the admin filter sidebar.
    Set the year_filter attr in the model:

    my_model_field.year_filter = True
    """

    def __init__(self, f, request, params, model, model_admin):
        super(YearFilterSpec, self).__init__(f, request, params, model, model_admin)
        today = datetime.now()
        self.links = [ (_('Any'), {}), ]

        # TODO: should be cleverer about the range, and get the
        # extents from the DB.
        for year in range(2011,1995,-1):
            self.links.append( ((str(year)), {'%s__year' % self.field.name: str(year), }) )


    def title(self):
        return "Year"

# Register the filter
FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'year_filter', False), YearFilterSpec) )

