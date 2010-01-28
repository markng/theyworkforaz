
from south.db import db
from django.db import models
from reps.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'House'
        db.create_table('reps_house', (
            ('id', orm['reps.house:id']),
            ('name', orm['reps.house:name']),
        ))
        db.send_create_signal('reps', ['House'])
        
        # Adding field 'Representative.house'
        db.add_column('reps_representative', 'house', orm['reps.representative:house'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'House'
        db.delete_table('reps_house')
        
        # Deleting field 'Representative.house'
        db.delete_column('reps_representative', 'house_id')
        
    
    
    models = {
        'reps.bill': {
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'short_title': ('django.db.models.fields.TextField', [], {})
        },
        'reps.district': {
            'area': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'reps.house': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'reps.party': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'reps.representative': {
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.District']"}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Party']"})
        },
        'reps.vote': {
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': "'20'", 'db_index': 'True'}),
            'voted_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }
    
    complete_apps = ['reps']
