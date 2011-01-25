from django.conf.urls.defaults import *
import os
from django.conf import settings
from haystack.views import SearchView, search_view_factory
from haystack.query import SearchQuerySet
from haystack.forms import SearchForm

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
admin.autodiscover()

sqs = SearchQuerySet()

urlpatterns = patterns('',
    # Example:
    # (r'^theyworkforaz/', include('theyworkforaz.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^images/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'media/images')}, 'images'),
    (r'^stylesheets/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'media/stylesheets')}),
    (r'^', include('reps.urls')),
    (r'^search/', include('haystack.urls')),
    (r'^accounts/', include('registration.urls')),
)

urlpatterns += patterns('haystack.views',
    url(r'^search/whole$', search_view_factory(
        view_class=SearchView,
        searchqueryset=sqs,
        form_class=SearchForm
    ), name='haystack_search'),
)
