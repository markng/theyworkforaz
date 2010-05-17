from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


# Create your models here.
class District(geomodels.Model):
    """a voting district"""
    id = geomodels.IntegerField("District ID", primary_key=True) # override default ID field, as we don't want autoincrement
    area = geomodels.MultiPolygonField()
    objects = geomodels.GeoManager()

    @models.permalink
    def get_absolute_url(self):
        return('reps.views.district', [str(self.id)])

    def __unicode__(self):
        """unicode representation"""
        return str(self.id)

class RepresentativeManager(models.Manager):
    """representative manager, add selects by party for templates, etc"""
    use_for_related_fields = True
    def democrats(self):
        """add a filter for democrats"""
        return self.filter(party__code='D')
    
    def republicans(self):
        """add a filter for republicans"""
        return self.filter(party__code='R')
    
class Representative(models.Model):
    """a representative (either house or senate)"""
    # alot of this stuff is nullable for when reps leave office
    id = models.IntegerField("Representative ID", primary_key=True) # override default so we can keep azleg ids
    name = models.CharField("Name", max_length=255)
    role = models.CharField("Role", max_length=255, blank=True, null=True)
    party = models.ForeignKey('Party')
    email = models.EmailField("Email", blank=True, null=True)
    room = models.CharField("Room", max_length=255, blank=True, null=True)
    phone = models.CharField("Phone", max_length=255, blank=True, null=True)
    fax = models.CharField("Fax", max_length=255, blank=True, null=True)
    district = models.ForeignKey('District', blank=True, null=True) 
    house = models.ForeignKey('House', blank=True, null=True)
    current = models.BooleanField('Current House Member', default=True)
    link = models.URLField('Link to Bio', blank=True, null=True) # not sure if azleg will remove bios after left
    objects = RepresentativeManager()

    @models.permalink
    def get_absolute_url(self):
        if self.house.name == 'House':
            return('reps.views.housemember', [str(self.id)])
        elif self.house.name == 'Senate':
            return('reps.views.senator', [str(self.id)])

    def __unicode__(self):
        """unicode representation"""
        return self.name

class House(models.Model):
    """a legislative house"""
    name = models.CharField("Name", max_length=255, blank=True, null=True)
    code = models.CharField("Short Code", max_length=1, unique=True)
    def __unicode__(self):
        """unicode representation"""
        if self.name:
            return self.name
        else:
            return self.code


class Party(models.Model):
    """political party"""
    name = models.CharField("Name", max_length=255, blank=True, null=True)
    code = models.CharField("Short Code", max_length=1, unique=True)
    class Meta:
        verbose_name_plural = "parties"

    def __unicode__(self):
        """unicode representation"""
        if self.name:
            return self.name
        else:
            return self.code

class SponsorshipManager(models.Manager):
    """sponsorship manager"""
    use_for_related_fields = True
    
    def republicans(self):
        """return only republicans"""
        return self.filter(representative__party__code='R')
    
    def democrats(self):
        """return only democrats"""
        return self.filter(representative__party__code='D')

class Sponsorship(models.Model):
    """sponsoring a bill"""
    representative = models.ForeignKey('Representative')
    bill = models.ForeignKey('Bill')
    type = models.CharField(max_length=10)
    objects = SponsorshipManager()
    
    def __unicode__(self):
        """string rep"""
        return "%s %s %s" % (str(self.representative), self.type, str(self.bill))

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
    short_title = models.TextField("Short Title", blank=True)

    def __unicode__(self):
        """unicode representation"""
        if self.short_title:
            return self.short_title
        else:
            return self.id

class BillDocument(models.Model):
    """model for a document associated to a bill"""
    url = models.URLField("Source URL", primary_key=True) # use the source URL for the Document as primary key
    type = models.CharField("Document Type", max_length=255) # document type, eg "Bill Revision", "House Agenda", "Fact Sheet"
    found_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    document = models.TextField()
    bill = models.ForeignKey(Bill)
    
    def __unicode__(self):
        """unicode/str rep"""
        return "%s %s" % (self.title, str(self.bill))