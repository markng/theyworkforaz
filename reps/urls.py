from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'reps.views.home', {}, 'home'),
)