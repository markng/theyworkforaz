from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from models import District, Representative, Bill, Place
from forms import WhereForm
from django.contrib.gis.geos import Point
from django.views.decorators.cache import cache_page
from django.contrib.gis.maps.google.overlays import GPolygon
from django.contrib.gis.maps.google.gmap import GoogleMap
from django.template import RequestContext
from haystack.query import SearchQuerySet

def home(request):
    """home page"""
    gmap = GoogleMap()
    return render_to_response('index.html', { 'gmap' : gmap }, context_instance=RequestContext(request))

def addresschecker(request):
    """go to district from address"""
    totemplate = {}
    if request.method == 'POST':
        form = WhereForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['lon'] and form.cleaned_data['lat']:
                location = (form.cleaned_data['lon'], form.cleaned_data['lat'])
                request.session['location'] = location
            if form.cleaned_data['district_id']:
                district = District.objects.get(id=form.cleaned_data['district_id'])
                return HttpResponseRedirect(district.get_absolute_url())
            elif form.cleaned_data['place_id']:
                place = Place.objects.get(pk=form.cleaned_data['place_id'])
                return HttpResponseRedirect(place.get_absolute_url())
        else:
            if form.errors['place_id']:
                totemplate['placesearch'] = SearchQuerySet().filter(content=request.POST['where']).filter(django_ct="reps.place") # ugh.
        totemplate['form'] = form
    else:
        totemplate['form'] = WhereForm()
    return render_to_response('address.html', totemplate, context_instance=RequestContext(request))

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
    totemplate['boundary_close'] = False
    slocation = Point(request.session.get('location', False))
    if slocation and district.area.contains(slocation):
        poly = GPolygon(district.area[0])
        gmap = GoogleMap(polygons=[poly], markers=[slocation])
        if district.area.boundary.distance(slocation) < 0.01:
            totemplate['boundary_close'] = True
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
    
def global_forms_context_processor(request):
    from haystack.forms import SearchForm
    from haystack.query import SearchQuerySet
    sqs = SearchQuerySet()
    to_context = {}
    to_context['search_form'] = SearchForm(searchqueryset=sqs)
    to_context['where_form'] = WhereForm()
    return to_context
