from django.contrib.auth.models import User
from django.db import models

CHOICES = (
    ('Manual', 'Manual'),
    ('Automatic', 'Automatic'),
)

LOC = (
    ('Los Angeles', 'Los Angeles'),
    ('Chicago', 'Chicago'),
    ('New York',  'New York'),
)


# Create your models here.
class Car(models.Model):
    picture = models.FileField(null=True)
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    car_make = models.CharField(max_length=100, null=True)
    price = models.IntegerField(null=True)
    commision = models.IntegerField(default=0, null=True)
    fuel = models.CharField(max_length=20, null=True)
    dimensions = models.CharField(max_length=50, null=True)
    transmission = models.CharField(max_length= 50, choices=CHOICES)
    location = models.CharField(max_length=100, null=True, choices=LOC)
    gears = models.IntegerField(null=True)
    seats = models.IntegerField(null=True)
    power = models.IntegerField(null=True)
    tank_capacity = models.IntegerField(null=True)
    engine_displacement = models.IntegerField(null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField()

    def total_price(self):
        return self.price + self.commision

    def __str__(self):
        return self.brand + " " + self.name


class TestDrive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    time = models.DateField()
    license = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' - ' + self.car.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    address = models.TextField()
    license = models.TextField()
    insurance = models.IntegerField()
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='approved_by_user')
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' - ' + self.car.name
