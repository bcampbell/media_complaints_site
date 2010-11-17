# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Entity'
        db.create_table('cases_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('cases', ['Entity'])

        # Adding model 'Tag'
        db.create_table('cases_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('cases', ['Tag'])

        # Adding model 'Clause'
        db.create_table('cases_clause', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('prettyname', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('cases', ['Clause'])

        # Adding model 'Outcome'
        db.create_table('cases_outcome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('cases', ['Outcome'])

        # Adding model 'Article'
        db.create_table('cases_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=512, blank=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('pubdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='articles_published', null=True, to=orm['cases.Entity'])),
        ))
        db.send_create_signal('cases', ['Article'])

        # Adding M2M table for field authors on 'Article'
        db.create_table('cases_article_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['cases.article'], null=False)),
            ('entity', models.ForeignKey(orm['cases.entity'], null=False))
        ))
        db.create_unique('cases_article_authors', ['article_id', 'entity_id'])

        # Adding model 'Case'
        db.create_table('cases_case', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('checked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('complaint_body', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cases_as_complaint_body', to=orm['cases.Entity'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_of_complaint', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('complaint', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('legacy_id', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('report', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('date_of_decision', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('outcome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cases.Outcome'], null=True)),
            ('url_of_complaint', self.gf('django.db.models.fields.URLField')(max_length=512, blank=True)),
            ('date_scraped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('cases', ['Case'])

        # Adding M2M table for field complainants on 'Case'
        db.create_table('cases_case_complainants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('case', models.ForeignKey(orm['cases.case'], null=False)),
            ('entity', models.ForeignKey(orm['cases.entity'], null=False))
        ))
        db.create_unique('cases_case_complainants', ['case_id', 'entity_id'])

        # Adding M2M table for field defendants on 'Case'
        db.create_table('cases_case_defendants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('case', models.ForeignKey(orm['cases.case'], null=False)),
            ('entity', models.ForeignKey(orm['cases.entity'], null=False))
        ))
        db.create_unique('cases_case_defendants', ['case_id', 'entity_id'])

        # Adding M2M table for field offending_articles on 'Case'
        db.create_table('cases_case_offending_articles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('case', models.ForeignKey(orm['cases.case'], null=False)),
            ('article', models.ForeignKey(orm['cases.article'], null=False))
        ))
        db.create_unique('cases_case_offending_articles', ['case_id', 'article_id'])

        # Adding M2M table for field tags on 'Case'
        db.create_table('cases_case_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('case', models.ForeignKey(orm['cases.case'], null=False)),
            ('tag', models.ForeignKey(orm['cases.tag'], null=False))
        ))
        db.create_unique('cases_case_tags', ['case_id', 'tag_id'])

        # Adding M2M table for field clauses on 'Case'
        db.create_table('cases_case_clauses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('case', models.ForeignKey(orm['cases.case'], null=False)),
            ('clause', models.ForeignKey(orm['cases.clause'], null=False))
        ))
        db.create_unique('cases_case_clauses', ['case_id', 'clause_id'])

        # Adding M2M table for field related_cases on 'Case'
        db.create_table('cases_case_related_cases', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_case', models.ForeignKey(orm['cases.case'], null=False)),
            ('to_case', models.ForeignKey(orm['cases.case'], null=False))
        ))
        db.create_unique('cases_case_related_cases', ['from_case_id', 'to_case_id'])

        # Adding M2M table for field related_links on 'Case'
        db.create_table('cases_case_related_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('case', models.ForeignKey(orm['cases.case'], null=False)),
            ('article', models.ForeignKey(orm['cases.article'], null=False))
        ))
        db.create_unique('cases_case_related_links', ['case_id', 'article_id'])

        # Adding model 'Detail'
        db.create_table('cases_detail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('case', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cases.Case'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('cases', ['Detail'])


    def backwards(self, orm):
        
        # Deleting model 'Entity'
        db.delete_table('cases_entity')

        # Deleting model 'Tag'
        db.delete_table('cases_tag')

        # Deleting model 'Clause'
        db.delete_table('cases_clause')

        # Deleting model 'Outcome'
        db.delete_table('cases_outcome')

        # Deleting model 'Article'
        db.delete_table('cases_article')

        # Removing M2M table for field authors on 'Article'
        db.delete_table('cases_article_authors')

        # Deleting model 'Case'
        db.delete_table('cases_case')

        # Removing M2M table for field complainants on 'Case'
        db.delete_table('cases_case_complainants')

        # Removing M2M table for field defendants on 'Case'
        db.delete_table('cases_case_defendants')

        # Removing M2M table for field offending_articles on 'Case'
        db.delete_table('cases_case_offending_articles')

        # Removing M2M table for field tags on 'Case'
        db.delete_table('cases_case_tags')

        # Removing M2M table for field clauses on 'Case'
        db.delete_table('cases_case_clauses')

        # Removing M2M table for field related_cases on 'Case'
        db.delete_table('cases_case_related_cases')

        # Removing M2M table for field related_links on 'Case'
        db.delete_table('cases_case_related_links')

        # Deleting model 'Detail'
        db.delete_table('cases_detail')


    models = {
        'cases.article': {
            'Meta': {'ordering': "('pubdate',)", 'object_name': 'Article'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'articles_authored'", 'blank': 'True', 'to': "orm['cases.Entity']"}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pubdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'articles_published'", 'null': 'True', 'to': "orm['cases.Entity']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'})
        },
        'cases.case': {
            'Meta': {'ordering': "('-date_of_decision',)", 'object_name': 'Case'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clauses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cases.Clause']", 'symmetrical': 'False', 'blank': 'True'}),
            'complainants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cases_as_complainant'", 'symmetrical': 'False', 'to': "orm['cases.Entity']"}),
            'complaint': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'complaint_body': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cases_as_complaint_body'", 'to': "orm['cases.Entity']"}),
            'date_of_complaint': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_decision': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_scraped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'defendants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cases_as_defendant'", 'symmetrical': 'False', 'to': "orm['cases.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'offending_articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'cases_as_offending_article'", 'blank': 'True', 'to': "orm['cases.Article']"}),
            'outcome': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cases.Outcome']", 'null': 'True'}),
            'related_cases': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_cases_rel_+'", 'blank': 'True', 'to': "orm['cases.Case']"}),
            'related_links': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'cases_as_related_link'", 'blank': 'True', 'to': "orm['cases.Article']"}),
            'report': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cases.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'url_of_complaint': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'})
        },
        'cases.clause': {
            'Meta': {'ordering': "('ident',)", 'object_name': 'Clause'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'prettyname': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'cases.detail': {
            'Meta': {'object_name': 'Detail'},
            'case': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cases.Case']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'cases.entity': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Entity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cases.outcome': {
            'Meta': {'object_name': 'Outcome'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'cases.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['cases']
