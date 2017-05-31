from django.conf.urls import url

from . import views

app_name = 'voters'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check_votable/(?P<voter_id>[0-9]+)/$', views.check_votable, name='check_votable')
]
