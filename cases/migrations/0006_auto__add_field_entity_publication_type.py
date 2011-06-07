# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Entity.publication_type'
        db.add_column('cases_entity', 'publication_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Entity.publication_type'
        db.delete_column('cases_entity', 'publication_type')


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
            'complainant_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'complainants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cases_as_complainant'", 'symmetrical': 'False', 'to': "orm['cases.Entity']"}),
            'complaint': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'complaint_body': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cases_as_complaint_body'", 'to': "orm['cases.Entity']"}),
            'correction_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'correction_page': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_complaint': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_decision': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_scraped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'defendants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cases_as_defendant'", 'symmetrical': 'False', 'to': "orm['cases.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'judgement': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'legacy_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'offending_articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'cases_as_offending_article'", 'blank': 'True', 'to': "orm['cases.Article']"}),
            'offending_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'offending_page': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'explanation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cases.Clause']", 'null': 'True', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publication_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'cases.outcome': {
            'Meta': {'object_name': 'Outcome'},
            'explanation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
