from django.db import models
from django.db.models.signals import m2m_changed

# TODO: add slug fields to things


class Entity( models.Model ):
    """ eg Fred Bloggs, The Daily Mail, Ofcom """
    name = models.CharField( max_length=255 )
    ENTITY_KIND_CHOICES = (
        ('p', 'Person'),
        ('c', 'Complaints Body'),
        ('m', 'Media'),
    )

    ENTITY_PUBLICATION_TYPE_CHOICES = (
        ('uklocal', 'UK local newspaper'),
        ('uknational', 'UK national newspaper'),
        ('ukmag', 'UK magazine'),
    )

    kind = models.CharField(max_length=8, choices=ENTITY_KIND_CHOICES)

    publication_type = models.CharField(max_length=16, blank=True, null=True, choices=ENTITY_PUBLICATION_TYPE_CHOICES)

    def num_uses(self):
        return self.cases_as_complaint_body.count() + self.cases_as_complainant.count() + self.cases_as_defendant.count() + self.articles_published.count() + self.articles_authored.count()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('entity-detail', (), { 'object_id': self.id })

    class Meta:
        ordering = ('name', )



class Tag( models.Model ):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tag-detail', (), { 'object_id': self.id })

    class Meta:
        ordering = ('name', )



class Clause( models.Model ):
    """ which code of conduct was (allegedly) violated """

    # eg PCC clause number, or OfCom rule
    ident = models.CharField(max_length=64, help_text="The PCC code eg '1'" )
    prettyname = models.CharField(max_length=512, help_text="eg 'Accuracy'")
    explanation = models.TextField( blank=True, help_text="Explanation of clause (markdown formatting)" )

    # subclauses have parent clauses
    parent = models.ForeignKey('self', blank=True, null=True )

    def __unicode__(self):
        if self.parent is not None:
            return unicode(self.parent) + u" - " + self.prettyname
        else:
            return self.prettyname

    @models.permalink
    def get_absolute_url(self):
        return ('clause-detail', (), { 'object_id': self.id })

    class Meta:
        ordering = ('ident', )



class Outcome( models.Model ):
    """ eg "resolved" "adjudicated" etc... """
    name = models.CharField( max_length=64 )
    explanation = models.TextField( blank=True, help_text="Explanation of outcome (markdown formatting)" )
    def __unicode__(self):
        return self.name

#    @models.permalink
#    def get_absolute_url(self):
#        return ('outcome-detail', (), { 'outcome_id': self.id })

class Article( models.Model ):
    """ a link to a newspaper article or web page """
    url = models.URLField(max_length=512, verify_exists=False, blank=True)
    headline = models.CharField( max_length=256, blank=True )
    pubdate = models.DateField(blank=True,null=True)
    publication = models.ForeignKey( Entity, related_name="articles_published", limit_choices_to={'kind':'m'}, null=True, blank=True )
    authors = models.ManyToManyField( Entity, related_name="articles_authored", limit_choices_to={'kind':'p'}, blank=True )

    def __unicode__(self):
        return u'%s ( %s )' % (self.headline, self.url)

    class Meta:
        ordering = ('pubdate', )



class Case(models.Model):
    """ an case reported to a body (eg someone complaining to the PCC) """
    checked = models.BooleanField()

    complaint_body = models.ForeignKey( Entity, related_name='cases_as_complaint_body', limit_choices_to={'kind':'c'}, help_text='The complaints body handling the case' )
    title = models.CharField( max_length=512, blank=True )
    summary = models.TextField(blank=True, help_text="short accessible summary of the complaint" )


    # TODO: need a better way to model complaints "on behalf of" and job titles etc...
    # eg "Ms Lucy McGee, Director of Communications for the West London Mental Health Trust v Sunday Express"
    complainants = models.ManyToManyField( Entity, related_name='cases_as_complainant', limit_choices_to={'kind':'p'}, help_text="Who made the complaint" )

    # TODO: complainant_type is a big bodge. Doesn't take into account the fact
    # that cases can have multiple complainants.
    # What should happen is that this info should be on the entity, and there
    # should be a proper way to model "on-behalf-of" relationships and job titles...
    COMPLAINANT_TYPE_CHOICES = (
        ('public_figure', 'Public Figure'),
        ('private_individual', 'Private Individual'),
        ('public_org', 'Public Sector Organisation'),
        ('private_org', 'Private Sector Organisation'),
        ('obo_public_figure', 'Solicitor on behalf of a Public Figure'), # (obo="on behalf of")
        ('obo_private_individual', 'Solicitor on behalf of a Private Individual'),
        ('obo_public_org', 'Solicitor on behalf of a Public Sector Organisation'),
        ('obo_private_org', 'Solicitor on behalf of a Private Sector Organisation'),

    )
    complainant_type = models.CharField( blank=True, max_length=32, choices=COMPLAINANT_TYPE_CHOICES, help_text="nature of complainant" )

    JUDGEMENT_CHOICES = (
        ('breach', "Newspaper appears to have breached the code"),
        ('nobreach', "Newspaper appears not to have breached the code"),
        ('denial', "Newspaper denies breaching the code and the PCC did not make a judgement"),
        ('nojudgement', "The PCC did not come to a judgement as to whether or not the code was breached"),
    )
    judgement = models.CharField( blank=True, max_length=16, choices=JUDGEMENT_CHOICES )

    # TODO: hmm... maybe should only support a single defendant?
    defendants = models.ManyToManyField( Entity,
        related_name='cases_as_defendant',
        limit_choices_to={'kind':'m'} )
    date_of_complaint = models.DateField(
        blank=True,
        null=True,
        help_text="When the complaint was lodged, if known" )

    complaint = models.TextField(blank=True)
    offending_articles = models.ManyToManyField( Article,
        blank=True,
        help_text="article(s) the complaint is about",
        related_name="cases_as_offending_article" )

    offending_page = models.IntegerField(null=True,blank=True,help_text="Page number of offending article in publication")
    offending_date = models.DateField(null=True,blank=True, help_text="Date the offending article was published" )
    correction_page = models.IntegerField(null=True,blank=True,help_text="Page number the correction appeared on, if any")
    correction_date = models.DateField(null=True,blank=True, help_text="Date the correction was published on, if any" )

    legacy_id = models.CharField( blank=True, null=True, max_length=256,
        help_text="eg article_id of the case as published in the PCC CMS system" )

    # for the PCC - the report number the case was published in
    report = models.CharField( max_length=32,
        blank=True,
        help_text="PCC report number the complaint was published in, if any" )

    tags = models.ManyToManyField( Tag, blank=True, help_text="Tags/Keywords" )
    clauses = models.ManyToManyField( Clause, blank=True  )

    # when a descision was published
    date_of_decision = models.DateField(blank=True, null=True, help_text="When the decision was made/published" )

    # enable custom admin filter
    date_of_decision.year_filter = True

    outcome = models.ForeignKey( Outcome, null=True )

    url_of_complaint = models.URLField(max_length=512, verify_exists=False, blank=True, help_text="The URL of the complaint on the PCC site")
    date_scraped = models.DateTimeField( blank=True,null=True )

    related_cases = models.ManyToManyField( "self",blank=True, help_text="Other complaints related to this one" )

    related_links = models.ManyToManyField( Article,
        blank=True,
        help_text="blogs posts, articles etc about this case",
        related_name="cases_as_related_link" )


#    def save(self, *args, **kwargs):
#        do_something()
#        super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
#        do_something_else()

    def root_clauses(self):
        """ shortcut to fetch all top-level clauses """
        return self.clauses.filter( parent=None )

    def time_to_decision(self):
        """ return time difference between offending article and decision being issued. Or None if unavailable. """
        if self.offending_date is None or self.date_of_decision is None:
            return None
        else:
            return self.date_of_decision - self.offending_date


    def __unicode__(self):
        return "%s - %s" % (self.id, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('case-detail', (), { 'object_id': self.id })

    class Meta:
        ordering = ('-date_of_decision', )


# we hook into the m2m_changed signal to detect when Case.clauses
# is being modififed.
# Whenever the clause list is changed, go through and add any missing
# parent clauses. So if you add a subclause, the main clause is
# automatically added too.

# evil nasty hackery to prevent infiniteloopagebadness
fiddle_case_clauses_LOCK = False

def fiddle_case_clauses(instance, action="post_add", reverse=False, pk_set=[], **kwargs ):
    """ ensure missing parent clauses are added """

    global fiddle_case_clauses_LOCK
    if fiddle_case_clauses_LOCK:
#        print "locked ",action, reverse,pk_set
        return

#    print "locked ",action, reverse,pk_set
    if action == 'post_add':

        existing_clauses = instance.clauses.all()
        missing_clauses = set()
        for c in existing_clauses:
            d = c
            while d.parent is not None:
                d = d.parent
                if d not in existing_clauses:
                    missing_clauses.add(d)

        fiddle_case_clauses_LOCK = True
#        print "missing clauses: ",missing_clauses
        if missing_clauses:
            instance.clauses.add(*missing_clauses)
        fiddle_case_clauses_LOCK = False





m2m_changed.connect( fiddle_case_clauses, sender=Case.clauses.through )




class Detail( models.Model ):
    case = models.ForeignKey( Case )
    content = models.TextField()
    kind = models.CharField( max_length=32, help_text="resolution or adjudication or whatever" )

