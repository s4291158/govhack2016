from django.conf.urls import url

from app.views import SchoolLocationsView, SchoolView, index_view

urlpatterns = [
    url(r'^$', index_view, name='index_view'),
    url(r'^school_locations/$', SchoolLocationsView.as_view(), name='school_locations'),
    url(r'^school/(?P<school_id>[0-9]+)/$', SchoolView.as_view(), name='school'),
]
