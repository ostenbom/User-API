from django.contrib import admin

from .models import Constituency, Station, Voter, Party, Candidate

admin.site.register(Constituency)
admin.site.register(Station)
admin.site.register(Voter)
admin.site.register(Party)
admin.site.register(Candidate)
