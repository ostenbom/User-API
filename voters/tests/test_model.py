import datetime
from django.test import TestCase

from ..models import Constituency, Station, Voter, Party, Candidate


def create_constituency():
    return Constituency(name="Brigg & Goole")


def create_station(constituency):
    return Station(name="Kensington Library", addr_line_1="53 Queen's Gate", addr_line_2="", postcode="SW7 3XZ", constituency=constituency)


def create_voter(station):
    return Voter(first_name="James", last_name="Bond", addr_line_1="007 Spy Street", addr_line_2="", postcode="SW7 7MQ", date_of_birth=datetime.date(1970, 7, 7), phone="+447654353205", station=station)

def create_party():
    return Party(name="Labour")

def create_candidate(constituency, party):
    return Candidate(first_name="Jeremy", last_name="Corbyn", constituency=constituency, party=party)


class ConstituencyModelTests(TestCase):

    def test_string_representation(self):
        constituency = create_constituency()
        self.assertEqual(str(constituency), constituency.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(Constituency._meta.verbose_name_plural), "constituencies")


class StationModelTests(TestCase):

    def test_string_representation(self):
        station = create_station(constituency=create_constituency())
        self.assertEqual(str(station), station.name)

    def test_delete_station_doesnt_delete_constituency(self):
        constituency = create_constituency()
        constituency.save()
        station = create_station(constituency)
        station.save()

        station.delete()
        saved_constituency = Constituency.objects.get(name=constituency.name)
        self.assertEqual(Station.objects.all().count(), 0)
        self.assertEqual(saved_constituency.name, constituency.name)


class VoterModelTests(TestCase):

    def test_string_representation(self):
        voter = create_voter(station=create_station(
            constituency=create_constituency()))
        self.assertEqual(str(voter), voter.first_name + ' ' + voter.last_name)

    def test_delete_voter_doesnt_delete_station(self):
        constituency = create_constituency()
        constituency.save()
        station = create_station(constituency)
        station.save()
        voter = create_voter(station)
        voter.save()

        voter.delete()
        saved_station = Station.objects.get(name=station.name)
        self.assertEqual(Voter.objects.all().count(), 0)
        self.assertEqual(saved_station.name, station.name)

class PartyModelTests(TestCase):

    def test_string_representation(self):
        party = create_party()
        self.assertEqual(str(party), party.name)

class CandidateModelTests(TestCase):

    def test_string_representation(self):
        candidate = create_candidate(constituency=create_constituency(), party=create_party())
        self.assertEqual(str(candidate), candidate.first_name + ' ' + candidate.last_name)

    def test_delete_candidate_doesnt_delete_party_and_constituency(self):
        constituency = create_constituency()
        constituency.save()
        party = create_party()
        party.save()
        candidate = create_candidate(constituency=constituency, party=party)
        candidate.save()

        candidate.delete()
        saved_party = Party.objects.get(name=party.name)
        saved_constituency = Constituency.objects.get(name=constituency.name)
        self.assertEqual(Candidate.objects.all().count(), 0)
        self.assertEqual(saved_party.name, party.name)
        self.assertEqual(saved_constituency.name, constituency.name)
