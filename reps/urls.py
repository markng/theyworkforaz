from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'reps.views.home', {}, 'home'),
    (r'^district/(?P<district_id>\d+)$', 'reps.views.district', {}, 'district'),
)