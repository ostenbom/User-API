from django.contrib import admin

from .models import Constituency, Station, Voter

admin.site.register(Constituency)
admin.site.register(Station)
admin.site.register(Voter)
