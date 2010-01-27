from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'reps.views.home', {}, 'home'),
    (r'^district/(?P<district>\d+)$', 'reps.views.district', {}, 'district'),
)