from django import forms
from django.conf import settings
from geocoders.google import geocoder
from reps.models import District
from django.contrib.gis.geos import Point

class WhereForm(forms.Form):
    """form for where a user lives"""
    where = forms.CharField(required=False, label="Where do you live ?", widget=forms.TextInput(attrs={'x-webkit-speech':True}))
    lat = forms.IntegerField(required=False, label="Latitude", widget=forms.HiddenInput())
    lon = forms.IntegerField(required=False, label="Longitude", widget=forms.HiddenInput())
    district_id = forms.IntegerField(required=False, label="District", widget=forms.HiddenInput())
    
    def clean(self):
        """clean attributes"""
        cleaned_data = self.cleaned_data
        where = cleaned_data.get('where')
        if where:
            geocode = geocoder(settings.GOOGLE_MAPS_API_KEY, lonlat=True)
            location = geocode(where)
            if location[0]:
                try:
                    district = District.objects.get(area__contains=Point(location[1]))
                    cleaned_data['district_id'] = district.id
                except District.DoesNotExist, e:
                    try:
                        location = geocode("%s, Arizona, USA" % (cleaned_data['where']))
                        district = District.objects.get(area__contains=Point(location[1]))
                        cleaned_data['district_id'] = district.id
                    except District.DoesNotExist, e:
                        self._errors['where'] = self.error_class(['We couldn\'t recognise that address - is it in Arizona?'])
            else:
                self._errors['where'] = self.error_class(['We couldn\'t recognise that address - is it a valid address?'])
            if location[1][0]:
                cleaned_data['lat'] = location[1][1]
                cleaned_data['lon'] = location[1][0]
        else:
            if not (cleaned_data.get('lat') and cleaned_data.get('lon')):
                self._errors['where'] = self.error_class(['Please fill in an address'])
        return cleaned_data