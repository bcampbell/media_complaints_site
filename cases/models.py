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

class Article( models.Model ):
    url = models.URLField(max_length=512, verify_exists=False, blank=True)
    headline = models.CharField( max_length=256, blank=True )
    pubdate = models.DateField(blank=True,null=True)
    publication = models.ForeignKey( Entity, related_name="articles_published", limit_choices_to={'kind':'c'}, null=True, blank=True )
    authors = models.ManyToManyField( Entity, related_name="articles_authored", limit_choices_to={'kind':'p'}, blank=True )

    def __unicode__(self):
        if self.url:
            return self.url
        else:
            return self.headline

class Case(models.Model):
    """ an case reported to a body (eg someone complaining to the PCC) """
    checked = models.BooleanField()

    complaint_body = models.ForeignKey( Entity, related_name='cases_as_complaint_body', limit_choices_to={'kind':'c'} )
    title = models.CharField( max_length=512, blank=True )
    summary = models.TextField(blank=True, help_text="short accessible summary of the complaint" )
    complainants = models.ManyToManyField( Entity, related_name='cases_as_complainant', limit_choices_to={'kind':'p'}, help_text="Who made the complaint" )
    defendants = models.ManyToManyField( Entity,
        related_name='cases_as_defendant',
        limit_choices_to={'kind':'m'} )
    date_of_complaint = models.DateField(
        blank=True,
        null=True,
        help_text="When the complaint was lodged" )

    complaint = models.TextField(blank=True)
    offending_articles = models.ManyToManyField( Article,
        blank=True,
        help_text="article(s) the complaint is about",
        related_name="cases_as_offending_article" )

    legacy_id = models.CharField(
        max_length=256,
        help_text="eg article_id of the case as published in the PCC CMS system" )

    # for the PCC - the report number the case was published in
    report = models.CharField( max_length=32,
        blank=True,
        help_text="PCC report number the complaint was published in, if any" )

    tags = models.ManyToManyField( Tag, blank=True, help_text="Tags/Keywords" )
    clauses = models.ManyToManyField( Clause, blank=True  )

    # when a descision was published
    date_of_decision = models.DateField(blank=True, null=True, help_text="When the decision was made/published" )

    outcome = models.ForeignKey( Outcome, null=True )

    url_of_complaint = models.URLField(max_length=512, verify_exists=False, blank=True, help_text="")
    date_scraped = models.DateTimeField( blank=True,null=True )

    related_cases = models.ManyToManyField( "self",blank=True, help_text="Other complaints related to this one" )

    related_links = models.ManyToManyField( Article,
        blank=True,
        help_text="blogs posts, articles etc about this case",
        related_name="cases_as_related_link" )

    def __unicode__(self):
        return "%s - %s" % (self.id, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('case-detail', (), { 'case_id': self.id })



class Detail( models.Model ):
    case = models.ForeignKey( Case )
    content = models.TextField()
    kind = models.CharField( max_length=32, help_text="resolution or adjudication or whatever" )

