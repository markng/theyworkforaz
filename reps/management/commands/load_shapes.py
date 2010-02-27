import os
from django.core.management.base import NoArgsCommand
from django.contrib.gis.utils.layermapping import LayerMapping
from django.conf import settings
from reps.models import District

class Command(NoArgsCommand):
    """command for loading shapes"""
    
    def handle_noargs(self, **options):        
        mapping = {
        'id' : 'DISTRICT',
        'area' : 'MULTIPOLYGON',
        }
        # this won't work if the app is renamed other than reps. Isn't there a better way?
        shp = os.path.abspath(os.path.join('reps', 'data', '2004legfinal_shp.shp'))
        lm = LayerMapping(District, shp, mapping, source_srs='NAD83')
        lm.save(strict=True, verbose=True)
