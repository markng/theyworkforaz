from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'reps.views.home', {}, 'home'),
    (r'^district/(?P<district_id>\d+)$', 'reps.views.district', {}, 'district'),
    (r'^senator/(?P<representative_id>\d+)$', 'reps.views.senator', {}, 'senator'),
    (r'^member/(?P<representative_id>\d+)$', 'reps.views.housemember', {}, 'senator'),
    (r'^bill/(?P<bill_id>.*)$', 'reps.views.bill', {}, 'bill'),
)