from django.http import JsonResponse, HttpResponse, HttpResponseForbidden

from .api_key_verification import valid_api_key

UNAUTHORIZED_CODE = 401

def verify(verif):
    def perform(func):
        def inner(request, **kwargs):
            # Does the user have an API key? (should also check they key is valid)
            if 'API_key' in request.COOKIES and valid_api_key(request.COOKIES['API_key']):
                # Does the user have appropriate permissions?
                if verif()(request.COOKIES['API_key']):
                    return func(request, **kwargs)
                return HttpResponseForbidden()
            return HttpResponse(status=UNAUTHORIZED_CODE)
        return inner
    return perform
