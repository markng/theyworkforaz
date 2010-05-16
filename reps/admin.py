from django.contrib.gis import admin as geoadmin
from django.contrib import admin
from models import District
from models import Representative
from models import Party
from models import Vote
from models import Bill
from models import House
from models import BillDocument

class BillDocumentAdmin(admin.ModelAdmin):
    list_filter = ('type',)

admin.site.register(District, geoadmin.OSMGeoAdmin)
admin.site.register(Representative)
admin.site.register(Party)
admin.site.register(Vote)
admin.site.register(Bill)
admin.site.register(House)
admin.site.register(BillDocument, BillDocumentAdmin)