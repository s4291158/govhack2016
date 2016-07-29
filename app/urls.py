from django.conf.urls import url

from app.views import SchoolLocationsView

urlpatterns = [
    url(r'^school_locations/$', SchoolLocationsView.as_view(), name='school_locations'),
]
