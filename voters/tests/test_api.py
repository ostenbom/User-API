import json
import datetime

from django.test import TestCase
from django.urls import reverse

from ..models import Constituency, Station, Voter
from ..views import check_votable

ELIGIBLE_VOTER_PK = 1
INELIGIBLE_VOTER_PK = 2
NON_EXIST_VOTER_PK = 23


def create_constituency():
    return Constituency.objects.create(name="Richmond Park")


def create_station(constituency):
    return Station.objects.create(name="", addr_line_1="", addr_line_2="", postcode="", constituency=constituency)


def create_eligible_voter(station):
    return Voter.objects.create(pk=ELIGIBLE_VOTER_PK, first_name="James", last_name="Bond", addr_line_1="007 Spy Street", addr_line_2="", postcode="SW7 7MQ", date_of_birth=datetime.date(1970, 7, 7), phone="+447654353205", station=station, used_vote=False)


def create_ineligable_voter(station):
    return Voter.objects.create(pk=INELIGIBLE_VOTER_PK, first_name="James", last_name="Bond", addr_line_1="007 Spy Street", addr_line_2="", postcode="SW7 7MQ", date_of_birth=datetime.date(1970, 7, 7), phone="+447654353205", station=station, used_vote=True)


class CheckVotabilityTests(TestCase):

    def test_endpoint_returns_response(self):
        url = reverse('voters:check_votable', args=(ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_eligible_voter_can_vote(self):
        create_eligible_voter(station=create_station(
            constituency=create_constituency()))
        url = reverse('voters:check_votable', args=(ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'voter_exists': True,
                                                'used_vote': False})

    def test_ineligible_cannot_vote(self):
        create_ineligable_voter(station=create_station(
            constituency=create_constituency()))
        url = reverse('voters:check_votable', args=(INELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'voter_exists': True,
                                                'used_vote': True})

    def test_non_existent_voter_returns_false(self):
        url = reverse('voters:check_votable', args=(NON_EXIST_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'voter_exists': False,
                                                'used_vote': None})
    # Invalid API user errors TODO
