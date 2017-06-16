import json
import datetime

from functools import partial

from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist

from .models import Voter, Candidate, Station, Constituency
from .api_key_verification import verify, has_check_votable_permissions,\
has_get_voters_permissions, has_make_voter_ineligible_permissions, \
has_get_candidates_permissions, has_set_voter_has_active_pin_permissions


def index(request):
    return HttpResponse("The Voter API is online.")


@verify(lambda: has_check_votable_permissions)
def check_votable(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
        return JsonResponse({'voter_exists': True,
                             'used_vote': voter.used_vote})
    except ObjectDoesNotExist:
        return JsonResponse({'voter_exists': False,
                             'used_vote': None})

@verify(lambda: has_get_voters_permissions)
def get_voters(request, station_id, voter_name, postcode):
    voters = Voter.objects.filter(
        station=station_id, first_name__icontains=voter_name, postcode__iexact=postcode)
    voters_json = json.loads(serializers.serialize("json", voters))
    return JsonResponse({'success': voters.count() > 0,
                         'voters': voters_json})

@verify(lambda: has_make_voter_ineligible_permissions)
def make_voter_ineligible(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
        voter.used_vote = True
        voter.save()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False})


@verify(lambda: has_set_voter_has_active_pin_permissions)
def set_voter_has_active_pin(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
        voter.active_pin = True
        voter.save()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False})


@verify(lambda: has_get_candidates_permissions)
def get_candidates(request, station_id):
    try:
        constituency = Station.objects.get(pk=station_id).constituency.pk
        candidates = Candidate.objects.filter(constituency=constituency)
        candidates_json = json.loads(serializers.serialize(
            "json", candidates, use_natural_foreign_keys=True))

        return JsonResponse({'success': candidates.count() > 0,
                             'candidates': candidates_json})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False,
                             'candidates': []})

def voter_turnout(request):
    constituencies = Constituency.objects.all()
    turnout = []

    for constituency in constituencies:
        registered_voters = 0
        num_voted = 0
        stations = Station.objects.filter(constituency=constituency)
        for station in stations:
            registered_voters += Voter.objects.filter(station=station).count()
            num_voted += Voter.objects.filter(used_vote=True, station=station).count()
        turnout.append({'constituency' : str(constituency),
                        'voted' : num_voted,
                        'registered_voters' : registered_voters})

    return JsonResponse({'turnout' : turnout})
