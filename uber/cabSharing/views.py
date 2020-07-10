import ast
import json

# Django API
from django.http import Http404
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response

from .service.ride import RideService
from . import models
from . import serializers


class RequestRide(generics.ListCreateAPIView):
    serializer_class = serializers.RequestSerializer

    def post(self, request, *args, **kwargs):
        context = {"request": self.request}
        data = ast.literal_eval(json.dumps(request.data))
        request_serializer = self.serializer_class(data=data, context=context)
        if request_serializer.is_valid():
            ride, error = RideService().book_ride(request_serializer, context)
            if error is not None:
                return Response({'detail': error.message}, status=error.status)
            return HttpResponse(ride, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RideStatus(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.RiderSerializer

    def get(self, request, *args, **kwargs):
        ride_id = self.kwargs.get('pk')
        try:
            ride_status = models.Ride.objects.filter(id=ride_id).values('status')
            return Response({'status': ride_status})
        except Exception as e:
            raise Http404

    def put(self, request, *args, **kwargs):

        context = {"request": self.request}
        data = ast.literal_eval(json.dumps(request.data))
        ride_serializer = self.serializer_class(data=data, context=context)
        if ride_serializer.is_valid():
            ride_data = ride_serializer.data
            ride_data = RideService().update_fare(ride_data)
            return Response(ride_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': ride_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Rider(generics.ListAPIView):
    serializer_class = serializers.RiderSerializer

    def post(self, request, *args, **kwargs):
        context = {"request": self.request}
        data = ast.literal_eval(json.dumps(request.data))
        rider_serializer = self.serializer_class(data=data, context=context)
        if rider_serializer.is_valid():
            rider_serializer.save()
            return Response(rider_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': rider_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = models.Rider.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        return Response({'results': data})


class Driver(generics.ListCreateAPIView):
    serializer_class = serializers.DriverSerializer

    def post(self, request, *args, **kwargs):
        context = {"request": self.request}
        data = ast.literal_eval(json.dumps(request.data))
        driver_serializer = self.serializer_class(data=data, context=context)
        if driver_serializer.is_valid():
            driver_serializer.save()
            return Response(driver_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': driver_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = models.Driver.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        return Response({'results': data})
