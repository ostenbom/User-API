from django.conf.urls import url

from . import views

POSTCODE_REGEX = '(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})'

app_name = 'voters'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check_votable/(?P<voter_id>[0-9]+)/$',
        views.check_votable, name='check_votable'),
    url(r'^get_voters/station_id/(?P<station_id>[0-9]+)/voter_name/(?P<voter_name>[A-z]+)/postcode/(?P<postcode>' +
        POSTCODE_REGEX + ')/$', views.get_voters, name='get_voters'),
    url(r'^make_voter_ineligible/(?P<voter_id>[0-9]+)/$',
        views.make_voter_ineligible, name='make_voter_ineligible'),
    url(r'^get_candidates/(?P<station_id>[0-9]+)/$',
        views.get_candidates, name='get_candidates')
]
