from django.db import models
from django.contrib.gis.db import models as geomodels

# Create your models here.
class District(geomodels.Model):
    """a voting district"""
    id = geomodels.IntegerField("District ID", primary_key=True) # override default ID field, as we don't want autoincrement
    area = geomodels.MultiPolygonField()
    objects = geomodels.GeoManager()


class Representative(models.Model):
    """a representative (either house or senate)"""
    name = models.CharField("Name", max_length=255)
    party = models.ForeignKey('Party')


class Party(models.Model):
    """political party"""
    name = models.CharField("Name", max_length=255)


class Vote(models.Model):
    """Vote for a bill"""
    VOTE_TYPES = (
        ('THIRD', 'A third vote'), # better explanation here
        ('MOTION', 'A motion'), # better explanation here
        # more types ?
    )
    representative = models.ForeignKey('Representative')
    bill = models.ForeignKey('Bill')
    vote = models.CharField(max_length="20", choices=VOTE_TYPES, db_index=True)
    voted_at = models.DateTimeField(db_index=True)


class Bill(models.Model):
    """a bill"""
    id = models.CharField("Bill ID", primary_key=True, max_length=255) # use the alphanumeric bill ID as primary key
    short_title = models.TextField("Short Title")
