from django.db import models


class Meter(models.Model):
    name = models.CharField(max_length=180)
    meter_key = models.CharField(primary_key=True, max_length=42)


class Measurement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    recorded_consumption = models.FloatField(null=True)
    measurement_key = models.AutoField(primary_key=True)
    meter_key = models.ForeignKey(Meter, on_delete=models.CASCADE, blank=True)

