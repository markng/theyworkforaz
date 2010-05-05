from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from geocoders.google import geocoder
from models import District
from forms import WhereForm
from django.contrib.gis.geos import Point
from django.contrib.gis.maps.google.overlays import GPolygon
from django.contrib.gis.maps.google.gmap import GoogleMap

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
    else:
        form = WhereForm()

    return render_to_response('index.html', { 'form' : form, })

def district(request, district_id=None):
    """district page"""
    totemplate = {}
    district = District.objects.get(id=district_id)
    totemplate['district'] = district
    poly = GPolygon(district.area[0])
    slocation = request.session.get('location', False)
    if slocation and district.area.contains(Point(slocation[1])):
        gmap = GoogleMap(polygons=[poly], markers=[Point(slocation[1])])
    else:
        gmap = GoogleMap(polygons=[poly])
    totemplate['gmap'] = gmap
    return render_to_response('district.html', totemplate)

def senator(request):
    """senator page"""
    return render_to_response('senator.html')

def housemember(request):
    """house member page"""
    return render_to_response('member.html')