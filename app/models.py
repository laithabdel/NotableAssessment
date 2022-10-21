import uuid

from django.utils import timezone
from django.db import models
from datetime import datetime


# Create your models here, feel free to add more

class Doctor(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)


class Patient(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)


class Appointment(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, null=True, to_field="id", on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, null=True, to_field="id", on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField(default=timezone.now)
    appointment_type = models.CharField(max_length=50, null=True)
