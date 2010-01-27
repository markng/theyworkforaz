from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from geocoders.google import geocoder
from models import District
from forms import WhereForm
from django.contrib.gis.geos import Point

def home(request):
    """home page"""
    if request.method == 'POST':
        form = WhereForm(request.POST)
        if form.is_valid():
            geocode = geocoder(settings.GOOGLE_MAPS_API_KEY, lonlat=True)
            location = geocode(form.cleaned_data['where'])
            try:
                district = District.objects.get(area__contains=Point(location[1]))
            except District.DoesNotExist, e:
                return render_to_response('index.html', { 'form' : form, }) # isn't in arizona. Handle better
            return HttpResponseRedirect(district.get_absolute_url())
    else:
        form = WhereForm()

    return render_to_response('index.html', { 'form' : form, })

def district(request, district=None):
    """district page"""
    return render_to_response('district.html')

def senator(request):
    """senator page"""
    return render_to_response('senator.html')

def housemember(request):
    """house member page"""
    return render_to_response('member.html')