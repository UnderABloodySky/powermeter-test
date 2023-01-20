from django.db.models import Max, Min, Sum, Avg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from test.models import Meter, Measurement
from test.serializers import MeterSerializer, MeasurementSerializer


class BasePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]


class APIViewWithMeter(APIView):

    @staticmethod
    def __get_meter_object__(a_meter_key):
        try:
            return Meter.objects.get(meter_key=a_meter_key)
        except Meter.DoesNotExist:
            return None

    def get_meter_or_404(self, a_meter_key):
        meter_instance = self.__get_meter_object__(a_meter_key)
        if not meter_instance:
            return Response(
                {"res": "Meter with this key does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = MeterSerializer(meter_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIViewWithMeMeasurement(APIViewWithMeter):
    serializer = MeasurementSerializer()

    def get_with(self, f, request, a_meter_key, *args, **kwargs):
        self.get_meter_or_404(a_meter_key)
        measurements_of_a_meter = Measurement.objects.filter(meter_key=a_meter_key)
        max_measurement = measurements_of_a_meter.aggregate(max_consumption=f)
        max_measurement = measurements_of_a_meter.filter(
            recorded_consumption=max_measurement['max_consumption']).first()
        if max_measurement is None:
            return Response(
                {"res": "The Meter hasn't any recorded consumption"},
                status=status.HTTP_400_BAD_REQUEST)
        serializer = MeasurementSerializer(max_measurement)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetConsumptionView(APIViewWithMeMeasurement):

    def get_with(self, f, request, a_meter_key, *args, **kwargs):
        self.get_meter_or_404(a_meter_key)
        measurements_of_a_meter = Measurement.objects.filter(meter_key=a_meter_key)
        total = measurements_of_a_meter.aggregate(total_consumption=f)

        total_consumption = 0 if total['total_consumption'] is None else total
        return Response(
            {"res": total_consumption},
            status=status.HTTP_200_OK)


class PostMeterAPIView(BasePostAPIView, APIViewWithMeter):

    @swagger_auto_schema(
        request_body=MeterSerializer,
        operation_description="Create a Meter",
        operation_id="Meter_create",
        responses={200: MeterSerializer}
    )
    def post(self, request, *args, **kwargs):
        a_meter_key = request.data.get('meter_key')
        data = {
            'name': request.data.get('name'),
            'meter_key': a_meter_key
        }
        serializer = MeterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMeterAPIView(APIViewWithMeter):

    @swagger_auto_schema(
        operation_description="Return a Meter whose key is a_meter_key",
        operation_id="Get_meter",
        responses={200: MeterSerializer}
    )
    def get(self, request, a_meter_key, *args, **kwargs):
        return self.get_meter_or_404(a_meter_key)


class PostMeasurementAPIView(BasePostAPIView, APIViewWithMeter):

    @swagger_auto_schema(
        request_body=MeasurementSerializer,
        operation_description='Create a Measurement for the Meter whose key is a_meter_key. The recorded consumption '
                              'should be > 0',
        operation_id="Create_measurement",
        responses={200: MeasurementSerializer}
    )
    def post(self, request, a_meter_key, *args, **kwargs):
        recorded_consumption = request.data.get('recorded_consumption')
        if recorded_consumption < 0:
            return Response({"res": "Recorded consumption is negative."},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        data = {"meter_key":a_meter_key,
                "recorded_consumption":recorded_consumption}
        serializer = MeasurementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMaxConsumptionAPIView(APIViewWithMeMeasurement):

    @swagger_auto_schema(
        operation_description="Return to the Measurement with Maximum consumption "
                              "of the meter whose key is a_meter_key",
        operation_id="Get_max_measurement",
        responses={200: MeasurementSerializer}
    )
    def get(self, request, a_meter_key, *args, **kwargs):
        return self.get_with(Max('recorded_consumption'), request, a_meter_key)


class GetMinConsumptionAPIView(APIViewWithMeMeasurement):

    @swagger_auto_schema(
        operation_description="Return to the Measurement with Minimum "
                              "consumption of the meter whose key is a_meter_key",
        operation_id="Get_min_measurement",
        responses={200: MeasurementSerializer}
    )
    def get(self, request, a_meter_key, *args, **kwargs):
        return self.get_with(Min('recorded_consumption'), request, a_meter_key)


class GetTotalConsumptionAPIView(GetConsumptionView):

    @swagger_auto_schema(
        operation_description="'Return to the total consumption of the meter whose key is a_meter_key'",
        operation_id="Get_total_consumption",
        responses={200: openapi.Schema(type=openapi.TYPE_NUMBER)}
    )
    def get(self, request, a_meter_key, *args, **kwargs):
        return self.get_with(Sum('recorded_consumption'), request, a_meter_key)


class GetAVGConsumptionAPIView(GetConsumptionView):

    @swagger_auto_schema(
        operation_description="'Return to the AVG consumption of the meter whose key is a_meter_key'",
        operation_id="Get_total_consumption",
        responses={200: openapi.Schema(type=openapi.TYPE_NUMBER)}
    )
    def get(self, request, a_meter_key, *args, **kwargs):
        return self.get_with(Avg('recorded_consumption'), request, a_meter_key)
