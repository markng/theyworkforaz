import os
from django.contrib.gis.utils.layermapping import LayerMapping
from models import District

mapping = {
    'id' : 'DISTRICT',
    'area' : 'MULTIPOLYGON',
}

shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/2004legfinal_shp.shp'))

def run(verbose=True):
    """run load geo data for arizona district shapes"""
    lm = LayerMapping(District, shp, mapping, source_srs='NAD83')
    lm.save(strict=True, verbose=verbose)