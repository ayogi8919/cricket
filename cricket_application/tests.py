from django.test import TestCase, Client
from .models import CricketTeam, MatchesFixture
from django.urls import reverse, resolve
from .views import *


class SampleTests(TestCase):
    def test_fields(self):
        team = CricketTeam()
        team.team_identifier = 'IND'
        team.team_name = 'INDIA'
        team.club_state = 'RGI STADIUM'
        team.save()
        record = CricketTeam.objects.get(pk=1)
        self.assertEqual(record, team)

    def test_home_url_is_resolved(self):
        url = reverse('cricket_application:home')
        self.assertEquals(resolve(url).func, MatchesView)

    def test_MatchFixture_list_GET(self):
        client = Client()
        response = client.get(reverse('cricket_application:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'match_fixture.html')
