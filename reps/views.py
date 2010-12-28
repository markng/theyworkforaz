from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from geocoders.google import geocoder
from models import District, Representative, Bill
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
    slocation = request.session.get('location', False)
    if slocation and district.area.contains(Point(slocation[1])):
        poly = GPolygon(district.area[0])
        gmap = GoogleMap(polygons=[poly], markers=[Point(slocation[1])])
    else:
        gmap = district.gmap()
    totemplate['gmap'] = gmap
    return render_to_response('district.html', totemplate)

def senator(request, representative_id=None):
    """senator page"""
    senator = get_object_or_404(Representative, pk=representative_id)
    return render_to_response('senator.html', { 'senator' : senator })

def housemember(request, representative_id=None):
    """house member page"""
    member = get_object_or_404(Representative.objects.select_related(), pk=representative_id)
    return render_to_response('member.html', { 'member' : member })

def bill(request, bill_id=None):
    """bill page"""
    bill = get_object_or_404(Bill.objects.select_related(), pk=bill_id)
    return render_to_response('bill.html', { 'bill' : bill })