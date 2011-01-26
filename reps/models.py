from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from haystack.forms import SearchForm
import datetime, isodate, pyquery
import pickle
from django.core.cache import cache
import logging
from django.contrib.gis.maps.google.overlays import GPolygon, GMarker, GIcon
from django.contrib.gis.maps.google.gmap import GoogleMap
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
import hashlib

logger = logging.getLogger(__name__)

MASK_BASE_COORDS = ((-20.0, -81.0), (-20.0, 85.0), (-150.0, 85.0), (-150.0, -81.0), (-20.0, -81.0))

# Create your models here.
class District(geomodels.Model):
    """a voting district"""
    id = geomodels.IntegerField("District ID", primary_key=True) # override default ID field, as we don't want autoincrement
    area = geomodels.MultiPolygonField()
    objects = geomodels.GeoManager()
    #sessions = models.ManyToManyField('Session')
    
    @models.permalink
    def get_absolute_url(self):
        return('reps.views.district', [str(self.id)])

    def __unicode__(self):
        """unicode representation"""
        return str(self.id)
        
    def balance(self):
        """return power balance"""
        balance = cache.get('district_%s_balance' % self.id)
        if not balance:
            reps = self.representative_set.select_related('house', 'party').all()
            balance = {
                'all' : {
                    'D' : 0,
                    'R' : 0,
                },
                'House' : {
                    'D' : 0,
                    'R' : 0,
                },
                'Senate' : {
                    'D' : 0,
                    'R' : 0,
                },
            }
            # do balance for all, house and senate
            for rep in reps:
                balance['all'][rep.party.code] = balance['all'][rep.party.code] + 1
                balance[rep.house.name][rep.party.code] = balance[rep.house.name][rep.party.code] + 1
            cache.set('district_%s_balance' % self.id, balance)
        return balance
    
    def gmap(self):
        """return a gmap object that we can use in templates"""
        gmap = cache.get('district_%s_gmap' % (self.id))
        if not gmap:
            area_polygons = []
            for polygon in self.area:
                area_polygons.append(GPolygon(polygon))
            gmap = GoogleMap(polygons=area_polygons)
            cache.set('district_%s_gmap' % (self.id), gmap)
        return gmap

    @property
    def color(self):
        """return a color code for this district"""
        m = hashlib.md5()
        m.update(self.area.wkt)
        md5s = m.hexdigest()
        return "#%s" % md5s[0:6]

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
    azleg_id = models.IntegerField("Representative ID")
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
    sessions = models.ManyToManyField('Session')
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
        
    def sponsored_bills(self):
        """return a queryset with sponsored bills"""
        return self.sponsorship_set.filter(type="P")

    def cosponsored_bills(self):
        """return a queryset with sponsored bills"""
        return self.sponsorship_set.filter(type="C")
    

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
    
    def primary(self):
        """return primary sponsors"""
        return self.filter(type="P")
    
    def cosponsors(self):
        """return cosponsors"""
        return self.filter(type="C")

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
    #session = models.ForeignKey('Session')
    short_title = models.TextField("Short Title", blank=True)

    def __unicode__(self):
        """unicode representation"""
        if self.short_title:
            return self.short_title
        else:
            return self.id
    
    @models.permalink
    def get_absolute_url(self):
        return('reps.views.bill', [str(self.id)])
    
    def official_url(self):
        """return official URL"""
        pass
            
class BillDocumentManager(models.Manager):
    """manager for bill docs"""
    def versions(self):
        """show only versions"""
        return self.filter(type="Versions")

class BillDocument(models.Model):
    """model for a document associated to a bill"""
    url = models.URLField("Source URL", primary_key=True) # use the source URL for the Document as primary key
    type = models.CharField("Document Type", max_length=255) # document type, eg "Bill Revision", "House Agenda", "Fact Sheet"
    found_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    document = models.TextField()
    bill = models.ForeignKey(Bill)
    objects = BillDocumentManager()
    
    def __unicode__(self):
        """unicode/str rep"""
        return "%s %s" % (self.title, str(self.bill))

class SessionManager(models.Manager):
    """manager for sessions"""
    def current_session(self):
        """return the current, or last session"""
        try:
            session = Session.objects.get(start__lt=datetime.datetime.now(), end__gt=datetime.datetime.now())
        except ObjectDoesNotExist, e:
            session = Session.objects.order_by('-start')[0]
        except Exception, e:
            raise e
        return session

class Session(models.Model):
    """model for a legislature session"""
    id = models.IntegerField(primary_key=True) # actual session ID
    name = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    objects = SessionManager()
    
    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)

    @models.permalink
    def get_absolute_url(self):
        return('session', [self.id])

    def from_session_dict(self, session):
        """
            from session xml dictionary
            {
                'Legislature': '49', 
                'Session_Start_Date': '2010-08-09T15:00:00', 
                'Session_ID': '103', 
                'Legislation_Year': '2010', 
                'Session': '9S', 
                'Sine_Die_Date': '2010-08-11T10:56:00', 
                'Session_Full_Name': 'Forty-ninth Legislature - Ninth Special Session'
            }
        """
        self.id = session['Session_ID']
        self.name = session['Session_Full_Name']
        self.year = session['Legislation_Year']
        self.start = isodate.parse_datetime(session['Session_Start_Date'])
        self.end = isodate.parse_datetime(session['Sine_Die_Date'])
        self.save()

class Place(geomodels.Model):
    """
    Place
    
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    feature_type = models.CharField(max_length=255, blank=True, null=True)
    area = geomodels.MultiPolygonField()
    districts = models.ManyToManyField('District')
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('place', [self.id])
    
    def in_districts(self):
        """return the districts that this place is in"""
        return District.objects.filter(area__intersects=self.area)
    
    def gmap(self):
        """return a gmap object that we can use in templates"""
        gmap = cache.get('place_%s_gmap' % (self.id))
        if not gmap:
            area_polygons = []
            area_markers = []
            districts = self.in_districts()
            for district in districts:
                area = district.area.difference(district.area.difference(self.area)) # find the part of the district that is inside the place ( district - (district - area))
                icon = GIcon('district_%d' % district.id, '/images/markers/marker%d.png' % district.id)
                try:
                    gp = GPolygon(area, stroke_color="#000", fill_color=district.color, fill_opacity="0.2")
                    area_polygons.append(gp)
                    marker = GMarker(area.centroid, icon=icon)
                    area_markers.append(marker)
                except Exception, e:
                    marker = GMarker(area[0].centroid, icon=icon)
                    area_markers.append(marker)
                    for poly in area:
                        gp = GPolygon(poly, stroke_color="#000", fill_color=district.color, fill_opacity="0.2")
                        area_polygons.append(gp)
            gmap = GoogleMap(polygons=area_polygons, markers=area_markers)
            cache.set('place_%s_gmap' % (self.id),gmap)
        return gmap