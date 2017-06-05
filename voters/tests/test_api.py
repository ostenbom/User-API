import json
import datetime

from django.test import TestCase
from django.urls import reverse

from ..models import Constituency, Station, Voter, Party, Candidate
from ..views import check_votable

ELIGIBLE_VOTER_PK = 1
INELIGIBLE_VOTER_PK = 2
NON_EXIST_VOTER_PK = 23
CANDIDATE_PK = 1
PARTY_PK = 1
STATION_PK = 1
INVALID_STATION_PK = 47
CONSTITUENCY_PK = 1
RESPONSE_OK = 200

ELIGIBLE_VOTER_JSON = json.dumps({'success': True,
                                  'voters':
                                  [{'pk': ELIGIBLE_VOTER_PK,
                                    'model': 'voters.voter',
                                    'fields': {'first_name': 'James',
                                               'last_name': 'Bond',
                                               'addr_line_1': '007 Spy Street',
                                               'addr_line_2': '',
                                               'postcode': 'SW7 3BH',
                                               'date_of_birth': '1970-07-07',
                                               'phone': '+447654353205',
                                               'used_vote': False,
                                               'station': STATION_PK}}]
                                  }, sort_keys=True)

CANDIDATE_JSON = json.dumps({'success': True,
                                  'candidates':
                                  [{'pk': CANDIDATE_PK,
                                    'model': 'voters.candidate',
                                    'fields': {'first_name': 'Jeremy',
                                               'last_name': 'Corbyn',
                                               'constituency': CONSTITUENCY_PK,
                                               'party' : PARTY_PK }}]
                                  }, sort_keys=True)


def create_constituency():
    return Constituency.objects.create(name="Richmond Park")


def create_station(constituency):
    return Station.objects.create(pk=STATION_PK, name="Kensington Library", addr_line_1="", addr_line_2="", postcode="SW7 3BH", constituency=constituency)


def create_eligible_voter(station):
    return Voter.objects.create(pk=ELIGIBLE_VOTER_PK, first_name="James", last_name="Bond", addr_line_1="007 Spy Street", addr_line_2="", postcode="SW7 3BH", date_of_birth=datetime.date(1970, 7, 7), phone="+447654353205", station=station, used_vote=False)


def create_ineligable_voter(station):
    return Voter.objects.create(pk=INELIGIBLE_VOTER_PK, first_name="James", last_name="Bond", addr_line_1="007 Spy Street", addr_line_2="", postcode="SW7 3BH", date_of_birth=datetime.date(1970, 7, 7), phone="+447654353007", station=station, used_vote=True)

def create_party():
    return Party.objects.create(pk=PARTY_PK, name="Labour")

def create_candidate(constituency, party):
    return Candidate.objects.create(pk=CANDIDATE_PK, first_name="Jeremy", last_name="Corbyn", constituency=constituency, party=party)


class CheckVotabilityTests(TestCase):

    def test_endpoint_returns_response(self):
        url = reverse('voters:check_votable', args=(ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    def test_eligible_voter_can_vote(self):
        create_eligible_voter(station=create_station(
            constituency=create_constituency()))
        url = reverse('voters:check_votable', args=(ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'voter_exists': True,
                                                'used_vote': False})

    def test_ineligible_cannot_vote(self):
        create_ineligable_voter(station=create_station(
            constituency=create_constituency()))
        url = reverse('voters:check_votable', args=(INELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'voter_exists': True,
                                                'used_vote': True})

    def test_non_existent_voter_returns_false(self):
        url = reverse('voters:check_votable', args=(NON_EXIST_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'voter_exists': False,
                                                'used_vote': None})
    # Invalid API user errors TODO


class GetVoterAPITests(TestCase):

    def test_endpoint_returns_response(self):
        url = reverse('voters:get_voters',  args=(
            NON_EXIST_VOTER_PK, "James", "TW9 4EQ",))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    def test_can_retrieve_voter_who_exists(self):
        create_eligible_voter(station=create_station(
            constituency=create_constituency()))
        url = reverse('voters:get_voters', args=(
            ELIGIBLE_VOTER_PK, "James", "SW7 3BH",))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, ELIGIBLE_VOTER_JSON)

    def test_retrieving_voter_who_does_not_exist_returns_false(self):
        create_eligible_voter(station=create_station(
            constituency=create_constituency()))
        url = reverse('voters:get_voters', args=(STATION_PK, "Jenny", "TW9 4EQ",))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'success': False,
                                                'voters': []})


class MakeVoterIneligibleAPITests(TestCase):

    def test_endpoint_returns_response(self):
        url = reverse('voters:make_voter_ineligible',
                      args=(ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    def test_make_existing_voter_ineligible(self):
        create_eligible_voter(station=create_station(
            constituency=create_constituency()))
        url = reverse('voters:make_voter_ineligible',
                      args=(ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'success': True})

    def test_make_non_existing_voter_ineligible(self):
        url = reverse('voters:make_voter_ineligible',
                      args=(NON_EXIST_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'success': False})


class CandidateAPITests(TestCase):

    def test_endpoint_returns_response(self):
        url = reverse('voters:get_candidates', args=(STATION_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    def test_endpoint_returns_candidates(self):
        constituency = create_constituency()
        station = create_station(constituency)
        create_candidate(constituency=constituency, party=create_party())
        url = reverse('voters:get_candidates', args=(STATION_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, CANDIDATE_JSON)

    def test_endpoint_returns_error_for_invalid_constituency(self):
        url = reverse('voters:get_candidates', args=(INVALID_STATION_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertEqual(response.content, json.dumps({'success': False,
                                            'candidates': []}, sort_keys=True))
