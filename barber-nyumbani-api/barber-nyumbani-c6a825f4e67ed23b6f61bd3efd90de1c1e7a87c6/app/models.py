from django.db import models
import datetime as dt

# cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


# service model
class Service(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


# barber model
class Barber(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    services = models.ManyToManyField(Service, blank=True, null=True)

    def __str__(self):
        return self.name


# appointment model
class Appointment(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(default=dt.date.today)
    # reschedule_date = models.DateField(default=dt.date.today)
    # reschedule_time = models.TimeField(default=dt.datetime.now)
    status = models.CharField(max_length=200, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
