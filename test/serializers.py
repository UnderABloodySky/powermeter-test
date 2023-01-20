from .models import Meter, Measurement
from rest_framework import serializers


class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = ['meter_key', 'name']


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['timestamp', 'recorded_consumption', 'meter_key', 'measurement_key']
