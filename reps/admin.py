from django.contrib.gis import admin
from models import District
from models import Representative
from models import Party
from models import Vote
from models import Bill
from models import House

admin.site.register(District, admin.OSMGeoAdmin)
admin.site.register(Representative)
admin.site.register(Party)
admin.site.register(Vote)
admin.site.register(Bill)
admin.site.register(House)
