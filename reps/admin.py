from django.contrib.gis import admin as geoadmin
from django.contrib import admin
from models import *

class BillDocumentAdmin(admin.ModelAdmin):
    list_filter = ('type',)

admin.site.register(District, geoadmin.OSMGeoAdmin)
admin.site.register(Representative)
admin.site.register(Party)
admin.site.register(Place, geoadmin.OSMGeoAdmin)
admin.site.register(Vote)
admin.site.register(Bill)
admin.site.register(House)
admin.site.register(BillDocument, BillDocumentAdmin)
admin.site.register(Session)