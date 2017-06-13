import json
import datetime

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Voter, Candidate, Station


def index(request):
    return HttpResponse("The Voter API is online.")


def check_votable(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
        return JsonResponse({'voter_exists': True,
                             'used_vote': voter.used_vote})
    except ObjectDoesNotExist:
        return JsonResponse({'voter_exists': False,
                             'used_vote': None})


def get_voters(request, station_id, voter_name, postcode):
    voters = Voter.objects.filter(
        station=station_id, first_name=voter_name, postcode=postcode)
    voters_json = json.loads(serializers.serialize("json", voters))

    print voters_json

    return JsonResponse({'success': voters.count() > 0,
                         'voters': voters_json})


def make_voter_ineligible(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
        voter.used_vote = True
        voter.save()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False})


def set_voter_has_active_pin(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
        voter.active_pin = True
        voter.save()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False})


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
