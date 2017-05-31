import json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Voter


def index(request):
    return HttpResponse("Hello, world. You're at the voter index.")


def check_votable(request, voter_id):
    try:
        voter = Voter.objects.get(pk=voter_id)
        return JsonResponse({'voter_exists': True,
                             'used_vote': voter.used_vote})
    except ObjectDoesNotExist:
        return JsonResponse({'voter_exists': False,
                             'used_vote': None})
