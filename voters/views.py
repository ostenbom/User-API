import json
import datetime

from functools import partial

from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist

from .models import Voter, Candidate, Station
from .api_key_verification import has_check_votable_permissions, has_get_voters_permissions, has_make_voter_ineligible_permissions, has_get_candidates_permissions
from .api_utils import verify

def index(request):
    return HttpResponse("Hello, world. You're at the voter index.")


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
        station=station_id, first_name=voter_name, postcode=postcode)
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
