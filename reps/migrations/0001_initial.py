
from south.db import db
from django.db import models
from reps.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Party'
        db.create_table('reps_party', (
            ('id', orm['reps.Party:id']),
            ('name', orm['reps.Party:name']),
        ))
        db.send_create_signal('reps', ['Party'])
        
        # Adding model 'Bill'
        db.create_table('reps_bill', (
            ('id', orm['reps.Bill:id']),
            ('short_title', orm['reps.Bill:short_title']),
        ))
        db.send_create_signal('reps', ['Bill'])
        
        # Adding model 'Vote'
        db.create_table('reps_vote', (
            ('id', orm['reps.Vote:id']),
            ('representative', orm['reps.Vote:representative']),
            ('bill', orm['reps.Vote:bill']),
            ('vote', orm['reps.Vote:vote']),
            ('voted_at', orm['reps.Vote:voted_at']),
        ))
        db.send_create_signal('reps', ['Vote'])
        
        # Adding model 'District'
        db.create_table('reps_district', (
            ('id', orm['reps.District:id']),
            ('area', orm['reps.District:area']),
        ))
        db.send_create_signal('reps', ['District'])
        
        # Adding model 'Representative'
        db.create_table('reps_representative', (
            ('id', orm['reps.Representative:id']),
            ('name', orm['reps.Representative:name']),
            ('party', orm['reps.Representative:party']),
        ))
        db.send_create_signal('reps', ['Representative'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Party'
        db.delete_table('reps_party')
        
        # Deleting model 'Bill'
        db.delete_table('reps_bill')
        
        # Deleting model 'Vote'
        db.delete_table('reps_vote')
        
        # Deleting model 'District'
        db.delete_table('reps_district')
        
        # Deleting model 'Representative'
        db.delete_table('reps_representative')
        
    
    
    models = {
        'reps.bill': {
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'short_title': ('django.db.models.fields.TextField', [], {})
        },
        'reps.district': {
            'area': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'reps.party': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'reps.representative': {
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
