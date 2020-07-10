import math

from django.db import transaction

from uber.cabSharing import serializers
from uber.cabSharing.error import Error
from .. import models


class RideService:
    serializer_class = serializers.RideSerializer

    def book_ride(self, request):
        available_cabs = models.Driver.objects.filter(status='available').all()
        if len(available_cabs) == 0:
            return None, Error('No cabs available')
        cab = self.find_nearest_cab(available_cabs, request.get('start_lat'), request.get('end_lat'))
        ride = models.Ride()
        ride.dest_lat = request.get('dest_lat')
        ride.start_lat = request.get('start_lat')
        ride.start_long = request.get('start_long')
        ride.dest_long = request.get('dest_long')
        ride.start_address = request.get('start_address')
        ride.end_address = request.get('end_address')
        ride.rider_id = request.get('rider_id')
        ride.driver_id = request.get('driver_id')
        ride.status = 'BOOKED'
        request.status = 'COMPLETED'
        error = None
        transaction.set_autocommit(False)
        try:
            ride.save()
            cab.save()
            request.save()
            transaction.commit()
            transaction.set_autocommit(True)
        except Exception as ex:
            transaction.rollback()
            transaction.set_autocommit(True)
            error = Error(ex)

        if error is not None:
            return None, error

        return ride, None

    def calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

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
            ride_data.fare = distance*10

        ride_data.save()
        return ride_data



