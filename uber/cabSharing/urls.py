from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^request/$', views.RequestRide.as_view(), name='request_ride'),
    url(r'^rideStatus/(?P<pk>[0-9]+)/$', views.RideStatus.as_view(), name='rideStatus'),
    url(r'^rider/$', views.Rider.as_view(), name='rider_list'),
    url(r'^driver/$', views.Driver.as_view(), name='driver_list')
]
