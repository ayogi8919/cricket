from django.contrib import admin
from . models import *

admin.site.site_header = 'Cricket Project Administration'

class Team(admin.ModelAdmin):
    list_display = ['team_identifier','team_name','team_logo','club_state']

admin.site.register(CricketTeam,Team)
admin.site.register(CricketPlayer)
admin.site.register(PlayerHistory)
admin.site.register(MatchesFixture)
admin.site.register(MatchVenues)
admin.site.register(Points)