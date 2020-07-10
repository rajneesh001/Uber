from rest_framework import serializers

from . import models


class RiderSerializer(serializers.ModelSerializer):
    rides = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Ride.objects.all())

    class Meta:
        model = models.Rider
        fields = {'name', 'username', 'image_url', 'created_at', 'updated_at', 'image_url', 'phone', 'email', 'rides'}


class DriverSerializer(serializers.ModelSerializer):
    rides = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Ride.objects.all())

    class Meta:
        model = models.Driver
        fields = {'name', 'cab_reg_num', 'image_url', 'created_at', 'updated_at', 'image_url', 'phone', 'email',
                  'long', 'lat', 'rides'}


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Request
        fields = {'start_long', 'start_lat', 'des_lat', 'des_long', 'start_address', 'created_at', 'updated_at', 'end_address', 'rider'}


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ride
        fields = {'start_lat', 'start_long', 'des_long', 'created_at', 'updated_at', 'des_lat',
                  'fare', 'start_address', 'status', 'distance'}
