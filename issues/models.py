from django.db import models

class Entity( models.Model ):
    """ eg Fred Bloggs, The Daily Mail, Ofcom """
    name = models.CharField( max_length=255 )
    ENTITY_KIND_CHOICES = (
        ('p', 'Person'),
        ('c', 'Complaints Body'),
        ('m', 'Media'),
    )
    kind = models.CharField( max_length=8, choices=ENTITY_KIND_CHOICES )
    def __unicode__(self):
        return self.name

class Keyword( models.Model ):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('keyword', (), { 'kw': self.name })

class ComplaintCode( models.Model ):

    clause = models.CharField(max_length=64)
    prettyname = models.CharField(max_length=512)
    def __unicode__(self):
        return u"%s (%s)" % (self.clause, self.prettyname)

    @models.permalink
    def get_absolute_url(self):
        return ('clause', (), { 'clause': self.clause })


class Issue(models.Model):
    """ an issue reported to a body (eg someone complaining to the PCC) """
    checked = models.BooleanField()
    complaint_body = models.ForeignKey( Entity, related_name='issue_complaint_bodies', limit_choices_to={'kind':'c'} )
    title = models.CharField( max_length=512 )
    complainants = models.ManyToManyField( Entity, related_name='issue_complainants', limit_choices_to={'kind':'p'} )
    about = models.ManyToManyField( Entity, related_name='issue_abouts', limit_choices_to={'kind':'m'}  )
    date_of_problem = models.DateField()
    description = models.TextField(blank=True)

    keywords = models.ManyToManyField( Keyword, blank=True )
    codes = models.ManyToManyField( ComplaintCode, blank=True  )

    response = models.TextField(blank=True)

    outcome_keyword = models.CharField(max_length=255,blank=True)

    decision_and_explanation = models.TextField(blank=True)

    date_of_decision = models.DateField(null=True)

    url_of_story = models.URLField(max_length=512, verify_exists=False, blank=True)
    url_of_complaint = models.URLField(max_length=512, verify_exists=False, blank=True)

    related = models.ManyToManyField( "self",blank=True )

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('issue-detail', (), { 'issue_id': self.id })

