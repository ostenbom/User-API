from django.conf.urls import url

from . import views

POSTCODE_REGEX = '(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2})'
ID_REGEX = '[0-9]+'
NAME_REGEX = '[A-z ,.\'-]+'

app_name = 'voters'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check_votable/(?P<voter_id>' + ID_REGEX + ')/$',
        views.check_votable, name='check_votable'),
    url(r'^get_voters/station_id/(?P<station_id>' + ID_REGEX + ')/voter_name/(?P<voter_name>' + NAME_REGEX + ')/postcode/(?P<postcode>' +
        POSTCODE_REGEX + ')/$', views.get_voters, name='get_voters'),
    url(r'^make_voter_ineligible/(?P<voter_id>' + ID_REGEX + ')/$',
        views.make_voter_ineligible, name='make_voter_ineligible'),
    url(r'^get_candidates/(?P<station_id>' + ID_REGEX + ')/$',
        views.get_candidates, name='get_candidates')
]
