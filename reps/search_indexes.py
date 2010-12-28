from haystack.indexes import *
from haystack import site
from models import *

class DistrictSearchIndex(ModelSearchIndex):
    class Meta:
        pass

class RepresentativeSearchIndex(ModelSearchIndex):
    class Meta:
        pass

class PlaceSearchIndex(ModelSearchIndex):
    class Meta:
        pass

class BillSearchIndex(ModelSearchIndex):
    class Meta:
        pass

site.register(District, DistrictSearchIndex)
site.register(Representative, RepresentativeSearchIndex)
site.register(Place, PlaceSearchIndex)
site.register(Bill, BillSearchIndex)