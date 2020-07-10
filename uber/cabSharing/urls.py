from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^request/$', views.RequestRide.as_view(), name='request_ride'),
    url(r'^rideStatus/(?P<pk>[0-9]+)/$', views.RideStatus.as_view(), name='rideStatus'),
    url(r'^Rider/$', views.Rider.as_view(), name='rider_list'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetails.as_view(), name='user_detail'),
    url(r'^driver/$', views.Driver.as_view(), name='driver_list')
]

from rest_framework.authtoken import views

# Authentication
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]
