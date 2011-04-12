from haystack.indexes import *
from haystack import site
from theyworkforaz.reps.models import *

class DistrictSearchIndex(ModelSearchIndex, RealTimeSearchIndex):
    class Meta:
        pass

class RepresentativeSearchIndex(ModelSearchIndex, RealTimeSearchIndex):
    class Meta:
        pass

class PlaceSearchIndex(ModelSearchIndex, RealTimeSearchIndex):
    class Meta:
        pass

class BillSearchIndex(ModelSearchIndex, RealTimeSearchIndex):
    class Meta:
        pass

site.register(District, DistrictSearchIndex)
site.register(Representative, RepresentativeSearchIndex)
site.register(Place, PlaceSearchIndex)
site.register(Bill, BillSearchIndex)