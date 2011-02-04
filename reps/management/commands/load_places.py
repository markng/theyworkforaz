import os
from django.core.management.base import NoArgsCommand
from django.contrib.gis.utils.layermapping import LayerMapping
from django.conf import settings
from reps.models import Place

class Command(NoArgsCommand):
    """command for loading places"""
    
    def handle_noargs(self, **options):
        mappings = {
            'tl_2009_04_zcta5.shp' : {
                'name' : 'ZCTA5CE',
                'area' : 'MULTIPOLYGON',
                'type' : 'Zip Code'
            },

            'tl_2009_04_cbsa.shp' : {
                'name' : 'NAME',
                'area' : 'MULTIPOLYGON',
                'type' : 'MSA',
            },

            'tl_2009_04_county.shp': {
                'name' : 'NAME',
                'area' : 'MULTIPOLYGON',
                'type' : 'County',
            },

            'tl_2009_04_cousub.shp' : {
                'name' : 'NAME',
                'area' : 'MULTIPOLYGON',
                'type' : 'County Subdivision',
            },

            'tl_2009_04_elsd.shp' : {
                'name' : 'NAME',
                'area' : 'MULTIPOLYGON',
                'type' : 'Elementary School District',
            },

            'tl_2009_04_place.shp' : {
                'name' : 'NAME',
                'area' : 'MULTIPOLYGON',
                'type' : 'Place',
            },

            'tl_2009_04_scsd.shp' : {
                'name' : 'NAME',
                'area' : 'MULTIPOLYGON',
                'type' : 'Secondary School District',
            },

            'tl_2009_04_unsd.shp' : {
                'name' : 'NAME',
                'area' : 'MULTIPOLYGON',
                'type' : 'Unified School District',
            },
        }
        for filename, mapping in mappings.iteritems():
            ty = mapping.pop('type')
            # this won't work if the app is renamed other than reps. Isn't there a better way?
            shp = os.path.abspath(os.path.join('reps', 'data', 'places', filename))
            lm = LayerMapping(Place, shp, mapping, source_srs='NAD83')
            lm.save(strict=True, verbose=True)
            places = Place.objects.filter(feature_type__isnull=True).update(feature_type=ty)
            
