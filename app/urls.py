from django.conf.urls import url

from app.views import SchoolLocationView

urlpatterns = [
    url(r'^school_locations/$', SchoolLocationView.as_view(), name='school_locations'),
]
