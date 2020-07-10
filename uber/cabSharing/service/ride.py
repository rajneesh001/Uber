import ast
import json
from math import sin, cos, sqrt, atan2, radians

from .. import models
from .. import serializers
from ..error import Error


class RideService:
    serializer_class = serializers.RideSerializer

    def book_ride(self, request_serializer, context):

        available_cabs = models.Driver.objects.filter(status='BOOKED').all()
        if len(available_cabs) == 0:
            return None, Error('No cabs available')
        request_serializer.save()
        request_data = request_serializer.data
        request_data = ast.literal_eval(json.dumps(request_data))
        cab = self.find_nearest_cab(available_cabs, request_data.get('start_lat'), request_data.get('start_long'))
        ride = models.Ride()
        ride.dest_lat = request_data.get('dest_lat')
        ride.start_lat = request_data.get('start_lat')
        ride.start_long = request_data.get('start_long')
        ride.dest_long = request_data.get('dest_long')
        ride.start_address = request_data.get('start_address')
        ride.end_address = request_data.get('end_address')
        ride.rider_id = request_data.get('rider')
        ride.driver_id = cab.id
        request_data['status'] = 'COMPLETED'
        error = None
        try:
            request_serializer = serializers.RequestSerializer(data=request_data, context=context)
            if request_serializer.is_valid():
                request_serializer.save()
            ride.save()
            cab.save()

        except Exception as ex:
            error = Error(ex)

        if error is not None:
            return None, error

        return ride, None

    def calculate_distance(self, x1, y1, x2, y2):

        # approximate radius of earth in km
        R = 6373.0
        lat1 = radians(float(x1))
        lon1 = radians(float(y1))
        lat2 = radians(float(x2))
        lon2 = radians(float(y2))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance

    def find_nearest_cab(self, available_cabs, start_lat, start_long):
        result = None
        booked_cab = None
        for cab in available_cabs:
            cab_lat = cab.lat
            cab_long = cab.long
            distance = RideService().calculate_distance(start_lat, cab_lat, start_long, cab_long)
            if result is None or distance < result:
                result = distance
                booked_cab = cab
        booked_cab.status = 'BOOKED'
        return booked_cab

    # assumption per unit distance 10 Rs
    def update_fare(self, ride_data):

        if ride_data.status == 'COMPLETED':
            start_lat = ride_data.start_lat
            start_long = ride_data.start_long
            dest_start = ride_data.dest_start
            dest_long = ride_data.dest_long
            distance = self.calculate_distance(start_lat, dest_start, start_long, dest_long)
            ride_data.distance = distance
            ride_data.fare = distance * 10

        ride_data.save()
        return ride_data
