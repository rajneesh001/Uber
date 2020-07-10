from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(null=True)
    phone = models.CharField(max_length=10, unique=True,
                             error_messages={"unique": "this phone number already being taken"})
    email = models.EmailField(max_length=100, unique=True, error_messages={"unique": "this email already being taken"})
    cab_reg_num = models.CharField(max_length=100)
    lat = models.CharField(max_length=50, null=True)
    long = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, default='AVAILABLE')


class Rider(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(null=True)
    phone = models.CharField(max_length=10, unique=True,
                             error_messages={"unique": "this phone number already being taken"})
    email = models.EmailField(max_length=100, unique=True, error_messages={"unique": "this email already being taken"})


class Ride(models.Model):
    start_lat = models.CharField(max_length=50)
    start_long = models.CharField(max_length=50)
    dest_long = models.CharField(max_length=50)
    dest_lat = models.CharField(max_length=50)
    fare = models.CharField(max_length=100, default=0)
    start_address = models.CharField(max_length=100)
    end_address = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="assigned")
    distance = models.CharField(max_length=50, null=True)
    rider = models.ForeignKey(Rider, related_name='rider_ride', on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, related_name='driver_ride', on_delete=models.CASCADE)


class Request(models.Model):
    start_lat = models.CharField(max_length=50)
    start_long = models.CharField(max_length=50)
    dest_lat = models.CharField(max_length=50)
    dest_long = models.CharField(max_length=50)
    start_address = models.CharField(max_length=100)
    end_address = models.CharField(max_length=100)
    rider = models.ForeignKey(Rider, related_name='rider_request', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='INITIATED')
