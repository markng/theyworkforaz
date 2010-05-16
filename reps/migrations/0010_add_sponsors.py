
from south.db import db
from django.db import models
from reps.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Sponsorship'
        db.create_table('reps_sponsorship', (
            ('id', orm['reps.sponsorship:id']),
            ('representative', orm['reps.sponsorship:representative']),
            ('bill', orm['reps.sponsorship:bill']),
            ('type', orm['reps.sponsorship:type']),
        ))
        db.send_create_signal('reps', ['Sponsorship'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Sponsorship'
        db.delete_table('reps_sponsorship')
        
    
    
    models = {
        'reps.bill': {
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'short_title': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'reps.billdocument': {
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Bill']"}),
            'document': ('django.db.models.fields.TextField', [], {}),
            'found_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'primary_key': 'True'})
        },
        'reps.district': {
            'area': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'reps.house': {
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'reps.party': {
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'reps.representative': {
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.District']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.House']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Party']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'reps.sponsorship': {
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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
