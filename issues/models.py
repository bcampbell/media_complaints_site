from django.db import models

# TODO: add slug fields to things


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

    @models.permalink
    def get_absolute_url(self):
        return ('entity-detail', (), { 'entity_id': self.id })


class Tag( models.Model ):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tag-detail', (), { 'tag': self.name })


class Clause( models.Model ):
    """ which code of conduct was (allegedly) violated """

    # eg PCC clause number, or OfCom rule
    ident = models.CharField(max_length=64)

    prettyname = models.CharField(max_length=512)
    # TODO: add:
    # - link to code of practice
    # - explanation text (use markdown)

    def __unicode__(self):
        return self.prettyname

    @models.permalink
    def get_absolute_url(self):
        return ('clause-detail', (), { 'clause_id': self.id })


class Outcome( models.Model ):
    """ eg "resolved" "adjudicated" etc... """
    name = models.CharField( max_length=64 )

    def __unicode__(self):
        return self.name

#    @models.permalink
#    def get_absolute_url(self):
#        return ('outcome-detail', (), { 'outcome_id': self.id })



class Issue(models.Model):
    """ an issue reported to a body (eg someone complaining to the PCC) """
    checked = models.BooleanField()


    complaint_body = models.ForeignKey( Entity, related_name='issue_complaint_bodies', limit_choices_to={'kind':'c'} )
    title = models.CharField( max_length=512, blank=True )
    complainants = models.ManyToManyField( Entity, related_name='issue_complainants', limit_choices_to={'kind':'p'} )
    complaining_about = models.ManyToManyField( Entity, related_name='issue_abouts', limit_choices_to={'kind':'m'}  )
    date_of_problem = models.DateField(null=True)
    description = models.TextField(blank=True)

    # eg article_id of the case as published in the PCC CMS system
    legacy_id = models.CharField( max_length=512 )

    # for the PCC - the report number the case was published in
    report = models.CharField( max_length=32, null=True )

    tags = models.ManyToManyField( Tag, blank=True )
    clauses = models.ManyToManyField( Clause, blank=True  )

    outcome = models.ForeignKey( Outcome, null=True )
    date_of_decision = models.DateField(null=True)


    url_of_story = models.URLField(max_length=512, verify_exists=False, blank=True)
    url_of_complaint = models.URLField(max_length=512, verify_exists=False, blank=True)

    related = models.ManyToManyField( "self",blank=True )

    def __unicode__(self):
        return "%s - %s" % (self.id, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('issue-detail', (), { 'issue_id': self.id })



class Detail( models.Model ):
    issue = models.ForeignKey( Issue )
    content = models.TextField()
    kind = models.CharField( max_length=32 )

