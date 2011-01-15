# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Representative.azleg_id'
        db.add_column('reps_representative', 'azleg_id', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding M2M table for field sessions on 'Representative'
        db.create_table('reps_representative_sessions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('representative', models.ForeignKey(orm['reps.representative'], null=False)),
            ('session', models.ForeignKey(orm['reps.session'], null=False))
        ))
        db.create_unique('reps_representative_sessions', ['representative_id', 'session_id'])

        # Changing field 'Representative.id'
        db.alter_column('reps_representative', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))


    def backwards(self, orm):
        
        # Deleting field 'Representative.azleg_id'
        db.delete_column('reps_representative', 'azleg_id')

        # Removing M2M table for field sessions on 'Representative'
        db.delete_table('reps_representative_sessions')

        # Changing field 'Representative.id'
        db.alter_column('reps_representative', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))


    models = {
        'reps.bill': {
            'Meta': {'object_name': 'Bill'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'short_title': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'reps.billdocument': {
            'Meta': {'object_name': 'BillDocument'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Bill']"}),
            'document': ('django.db.models.fields.TextField', [], {}),
            'found_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'primary_key': 'True'})
        },
        'reps.district': {
            'Meta': {'object_name': 'District'},
            'area': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'reps.house': {
            'Meta': {'object_name': 'House'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'reps.party': {
            'Meta': {'object_name': 'Party'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'reps.place': {
            'Meta': {'object_name': 'Place'},
            'area': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'districts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reps.District']", 'symmetrical': 'False'}),
            'feature_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'reps.representative': {
            'Meta': {'object_name': 'Representative'},
            'azleg_id': ('django.db.models.fields.IntegerField', [], {}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.District']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.House']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Party']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sessions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reps.Session']", 'symmetrical': 'False'})
        },
        'reps.session': {
            'Meta': {'object_name': 'Session'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'reps.sponsorship': {
            'Meta': {'object_name': 'Sponsorship'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'reps.vote': {
            'Meta': {'object_name': 'Vote'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': "'20'", 'db_index': 'True'}),
            'voted_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['reps']
