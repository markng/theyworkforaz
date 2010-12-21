from django.conf.urls.defaults import *
from models import Session

sessionquery = Session.objects.all()

urlpatterns = patterns('',
    (r'^$', 'reps.views.home', {}, 'home'),
    (r'^district/(?P<district_id>\d+)$', 'reps.views.district', {}, 'district'),
    (r'^senator/(?P<representative_id>\d+)$', 'reps.views.senator', {}, 'senator'),
    (r'^member/(?P<representative_id>\d+)$', 'reps.views.housemember', {}, 'senator'),
    (r'^bill/(?P<bill_id>.*)$', 'reps.views.bill', {}, 'bill'),
    (
        r'^session', 
        'django.views.generic.list_detail.object_list', 
        {
            'queryset' : sessionquery,
            'template_name' : 'sessions.html',
            'template_object_name' : 'session',
        }, 
        'sessions'),
)