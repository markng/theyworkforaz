from django.conf.urls.defaults import *
from models import Session, Place, Representative

sessionquery = Session.objects.all()
placequery = Place.objects.all()
senatequery = Representative.objects.all()
housequery = Representative.objects.all()
urlpatterns = patterns('',
    (r'^$', 'reps.views.home', {}, 'home'),
    (r'^address$', 'reps.views.addresschecker', {}, 'addresscheck'),
    (r'^map.js$', 'reps.views.homemap', {}, 'homemap'),
    (r'^district/(?P<district_id>\d+)$', 'reps.views.district', {}, 'district'),
    (r'^senator/(?P<representative_id>\d+)$', 'reps.views.senator', {}, 'senator'),
    (r'^member/(?P<representative_id>\d+)$', 'reps.views.housemember', {}, 'member'),
    (r'^bill/(?P<bill_id>.*)$', 'reps.views.bill', {}, 'bill'),
    (
        r'^bookmark$',
        'reps.views.bookmark',
        {},
        'bookmark',
    ),
    (
        r'^unbookmark$',
        'reps.views.unbookmark',
        {},
        'unbookmark',
    ),
    (
        r'^session$', 
        'django.views.generic.list_detail.object_list', 
        {
            'queryset' : sessionquery,
            'template_name' : 'sessions.html',
            'template_object_name' : 'session',
        }, 
        'sessions'),
        
    (
        r'^session/(?P<object_id>\d+)$',
        'django.views.generic.list_detail.object_detail',
        {
            'queryset' : sessionquery,
            'template_name' : 'session.html',
            'template_object_name' : 'session',
        }, 
        'session'),
    (
        r'^place/(?P<object_id>\d+)$',
        'django.views.generic.list_detail.object_detail',
        {
            'queryset' : placequery,
            'template_name' : 'place.html',
            'template_object_name' : 'place',
        }, 
        'place'),
   (
        r'^senate$',
        'django.views.generic.list_detail.object_list',
        {
            'queryset' : senatequery,
            'template_name' : 'senate.html',
            'template_object_name' : 'senate',
        },
        'senate'),

   (
        r'^house$',
        'django.views.generic.list_detail.object_list',
        {
            'queryset' : housequery,
            'template_name' : 'house.html',
            'template_object_name' : 'house',
        },
        'house'),

    (
        r'^about$',
        'django.views.generic.simple.direct_to_template',
        {
            'template' : 'about.html',
        },
        'about'),
    (
        r'^fsmap$',
        'django.views.generic.simple.direct_to_template',
        {
            'template' : 'fullscreenmap.html',
        },
        'fsmap'
    ),
    (
        r'^account$',
        'django.views.generic.simple.direct_to_template',
        {
            'template' : 'account/account.html',
        },
        'account',
    ),
    (
        r'^planned_features',
        'django.views.generic.simple.direct_to_template',
        {
            'template' : 'planned_features.html',
        },
        'planned_features',
    ),
)
