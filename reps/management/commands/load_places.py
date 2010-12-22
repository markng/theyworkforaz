import os
from django.core.management.base import NoArgsCommand
from django.contrib.gis.utils.layermapping import LayerMapping
from django.conf import settings
from reps.models import Place

class Command(NoArgsCommand):
    """command for loading places"""
    
    def handle_noargs(self, **options):
        mapping = {
        'name' : 'ZCTA5CE',
        'area' : 'MULTIPOLYGON',
        }
        # this won't work if the app is renamed other than reps. Isn't there a better way?
        shp = os.path.abspath(os.path.join('reps', 'data', 'places', 'tl_2009_04_zcta5.shp'))
        lm = LayerMapping(Place, shp, mapping, source_srs='NAD83')
        lm.save(strict=True, verbose=True)
