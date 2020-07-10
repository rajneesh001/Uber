from rest_framework import serializers

from . import models


class RiderSerializer(serializers.ModelSerializer):
    rides = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Rider
        fields = ('name', 'username', 'image_url', 'created_at', 'updated_at', 'phone', 'email', 'rides', 'id')

    def get_rides(self, obj):
        record = models.Ride.objects.filter(rider_id=obj.id).all()
        return RideSerializer(record, many=True).data


class DriverSerializer(serializers.ModelSerializer):
    rides = serializers.SerializerMethodField()

    class Meta:
        model = models.Driver
        fields = ('name', 'cab_reg_num', 'image_url', 'created_at', 'updated_at', 'phone', 'email',
                  'long', 'lat', 'rides','status', 'id')

    def get_rides(self, obj):
        return models.Ride.objects.filter(driver_id=obj.id).all()


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Request
        fields = (
            'start_long', 'start_lat', 'dest_lat', 'dest_long', 'start_address', 'created_at', 'updated_at',
            'end_address', 'rider', 'id', 'status')


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ride
        fields = ('start_lat', 'start_long', 'dest_long', 'created_at', 'updated_at', 'dest_lat',
                  'fare', 'start_address', 'status', 'distance', 'id')
