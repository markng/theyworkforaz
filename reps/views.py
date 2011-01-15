from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from geocoders.google import geocoder
from models import District, Representative, Bill
from forms import WhereForm
from django.contrib.gis.geos import Point
from django.views.decorators.cache import cache_page
from django.contrib.gis.maps.google.overlays import GPolygon
from django.contrib.gis.maps.google.gmap import GoogleMap
from django.template import RequestContext

def home(request):
    """home page"""
    if request.method == 'POST':
        form = WhereForm(request.POST)
        if form.is_valid():
            geocode = geocoder(settings.GOOGLE_MAPS_API_KEY, lonlat=True)
            location = geocode(form.cleaned_data['where'])
            request.session['location'] = location
            try:
                district = District.objects.get(area__contains=Point(location[1]))
            except District.DoesNotExist, e:
                try:
                    location = geocode("%s, Arizona, USA" % (form.cleaned_data['where']))
                    request.session['location'] = location
                    district = District.objects.get(area__contains=Point(location[1]))
                except District.DoesNotExist, e:
                    return render_to_response('index.html', { 'form' : form, })
            return HttpResponseRedirect(district.get_absolute_url())
    gmap = GoogleMap()
    return render_to_response('index.html', { 'gmap' : gmap }, context_instance=RequestContext(request))

@cache_page(60*24)
def homemap(request):
    """javascript map render"""
    districts = District.objects.all()
    district_areas = []
    for district in districts:
        district_areas.append(GPolygon(district.area[0]))
    gmap = GoogleMap(center=Point(-111.8408203125,34.3797125804622), zoom=7, polygons=district_areas)
    return render_to_response('index_map.js', {'gmap' : gmap}, context_instance=RequestContext(request))

def district(request, district_id=None):
    """district page"""
    totemplate = {}
    district = District.objects.get(id=district_id)
    totemplate['district'] = district
    slocation = request.session.get('location', False)
    if slocation and district.area.contains(Point(slocation[1])):
        poly = GPolygon(district.area[0])
        gmap = GoogleMap(polygons=[poly], markers=[Point(slocation[1])])
    else:
        gmap = district.gmap()
    totemplate['gmap'] = gmap
    return render_to_response('district.html', totemplate, context_instance=RequestContext(request))

def senator(request, representative_id=None):
    """senator page"""
    senator = get_object_or_404(Representative, pk=representative_id)
    return render_to_response('senator.html', { 'senator' : senator }, context_instance=RequestContext(request))

def housemember(request, representative_id=None):
    """house member page"""
    member = get_object_or_404(Representative.objects.select_related(), pk=representative_id)
    return render_to_response('member.html', { 'member' : member }, context_instance=RequestContext(request))

def bill(request, bill_id=None):
    """bill page"""
    bill = get_object_or_404(Bill.objects.select_related(), pk=bill_id)
    return render_to_response('bill.html', { 'bill' : bill }, context_instance=RequestContext(request))
    
def search_form_context_processor(request):
    from haystack.forms import SearchForm
    from haystack.query import SearchQuerySet
    sqs = SearchQuerySet()
    form = SearchForm(searchqueryset=sqs)
    return { 'search_form': form }