
from south.db import db
from django.db import models
from reps.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Representative.phone'
        db.add_column('reps_representative', 'phone', orm['reps.representative:phone'])
        
        # Adding field 'Representative.current'
        db.add_column('reps_representative', 'current', orm['reps.representative:current'])
        
        # Adding field 'Representative.room'
        db.add_column('reps_representative', 'room', orm['reps.representative:room'])
        
        # Adding field 'Representative.role'
        db.add_column('reps_representative', 'role', orm['reps.representative:role'])
        
        # Adding field 'Representative.link'
        db.add_column('reps_representative', 'link', orm['reps.representative:link'])
        
        # Adding field 'Representative.fax'
        db.add_column('reps_representative', 'fax', orm['reps.representative:fax'])
        
        # Adding field 'Representative.email'
        db.add_column('reps_representative', 'email', orm['reps.representative:email'])
        
        # Changing field 'Representative.district'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['reps.District'], null=True, blank=True))
        db.alter_column('reps_representative', 'district_id', orm['reps.representative:district'])
        
        # Changing field 'Representative.house'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['reps.House'], null=True, blank=True))
        db.alter_column('reps_representative', 'house_id', orm['reps.representative:house'])
        
        # Changing field 'Representative.id'
        # (to signature: django.db.models.fields.IntegerField(primary_key=True))
        db.alter_column('reps_representative', 'id', orm['reps.representative:id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Representative.phone'
        db.delete_column('reps_representative', 'phone')
        
        # Deleting field 'Representative.current'
        db.delete_column('reps_representative', 'current')
        
        # Deleting field 'Representative.room'
        db.delete_column('reps_representative', 'room')
        
        # Deleting field 'Representative.role'
        db.delete_column('reps_representative', 'role')
        
        # Deleting field 'Representative.link'
        db.delete_column('reps_representative', 'link')
        
        # Deleting field 'Representative.fax'
        db.delete_column('reps_representative', 'fax')
        
        # Deleting field 'Representative.email'
        db.delete_column('reps_representative', 'email')
        
        # Changing field 'Representative.district'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['reps.District']))
        db.alter_column('reps_representative', 'district_id', orm['reps.representative:district'])
        
        # Changing field 'Representative.house'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['reps.House']))
        db.alter_column('reps_representative', 'house_id', orm['reps.representative:house'])
        
        # Changing field 'Representative.id'
        # (to signature: django.db.models.fields.AutoField(primary_key=True))
        db.alter_column('reps_representative', 'id', orm['reps.representative:id'])
        
    
    
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
        'reps.vote': {
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reps.Representative']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': "'20'", 'db_index': 'True'}),
            'voted_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }
    
    complete_apps = ['reps']
