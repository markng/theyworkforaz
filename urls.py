from django.conf.urls.defaults import *
import os
from django.conf import settings
from haystack.views import SearchView, search_view_factory
from reps.views import TWFASearchView
from haystack.query import SearchQuerySet
from haystack.forms import SearchForm
from django.contrib.auth import login
from registration.signals import user_activated
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
    (r'^js/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'media/js')}),
    (r'^', include('reps.urls')),
    (r'^search/', include('haystack.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^', include('django.contrib.auth.urls')),
)

urlpatterns += patterns('haystack.views',
    url(r'^search/whole$', search_view_factory(
        view_class=TWFASearchView,
        searchqueryset=sqs,
        form_class=SearchForm
    ), name='haystack_search'),
)

def login_on_activation(sender, user, request, **kwargs):
    user.backend='django.contrib.auth.backends.ModelBackend'
    login(request,user)
user_activated.connect(login_on_activation)