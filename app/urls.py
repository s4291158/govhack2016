from django.conf.urls import url

from app.views import SchoolLocationsView, index_view

urlpatterns = [
    url(r'^$', index_view, name='index_view'),
    url(r'^school_locations/$', SchoolLocationsView.as_view(), name='school_locations'),
]
