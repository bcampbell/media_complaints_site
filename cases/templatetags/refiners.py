""" Helpers for rendering refiners, which are used to implement filters on the search page """


from django import template

from django.template import Library, Node, resolve_variable, TemplateSyntaxError
from django.template import Context, Template, Node, resolve_variable, TemplateSyntaxError, Variable

register = template.Library()
     
register = Library()

class RefinersNode(Node):
    # TODO: generalise:
    #   - assumption that empty set means "All"
    #   - multi selection/mutual exclusivity
    def __init__(self, name, refiners, currently_set):
        self.refiners = refiners
        self.name = name
        self.currently_set = currently_set
 
    def render(self, context):
        req = resolve_variable('request',context)

        refiner_list = Variable(self.refiners).resolve(context)
        current = set(Variable(self.currently_set).resolve(context))

        out = '';

        # we assume that empty set of selected values means "All"
        if current:
            out += '<li><a href="%s">All</a></li>\n' % (self.calc_url(req, set()),)
        else:
            out += '<li><strong>All</strong></a>\n';


        for r in refiner_list:
            out += '<li>'
            if r.value in current:
                # show link with this value removed
                foo = current.copy()
                foo.remove(r.value)
                url = self.calc_url(req, foo)
                out += '<strong>%s</strong><a href="%s"> [-]</a>' % (r.label,url)
            else:
                # show link with this value added
                foo = current.copy()
                foo.add(r.value)
                url = self.calc_url(req, foo)
                out += '<a href="%s">%s</a>' % (url,r.label)
            out += '</li>';
        return out

    def calc_url(self,req,values):
        params = req.GET.copy()
        params.setlist(self.name, list(values))
        return '?%s' %  params.urlencode()
        

# 
# {% refiner_list <paramname> <refiners> <currentvals> %}
# 
@register.tag
def refiner_list(parser, token):
    bits = token.contents.split()
#    if len(bits) != 5:
#        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
#    if bits[3] != 'as':
#        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return RefinersNode(bits[1],bits[2],bits[3])


