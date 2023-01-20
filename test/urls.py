from django.urls import path
from .views import (
    PostMeterAPIView, GetMeterAPIView, PostMeasurementAPIView, GetMaxConsumptionAPIView, GetMinConsumptionAPIView,
    GetTotalConsumptionAPIView, GetAVGConsumptionAPIView,
)

urlpatterns = [
    path('api/meter', PostMeterAPIView.as_view()),
    path('api/meter/<int:a_meter_key>/', GetMeterAPIView.as_view()),
    path('api/measurement/<int:a_meter_key>/', PostMeasurementAPIView.as_view()),
    path('api/measurement/<int:a_meter_key>/max', GetMaxConsumptionAPIView.as_view()),
    path('api/measurement/<int:a_meter_key>/min', GetMinConsumptionAPIView.as_view()),
    path('api/measurement/<int:a_meter_key>/total', GetTotalConsumptionAPIView.as_view()),
    path('api/measurement/<int:a_meter_key>/avg', GetAVGConsumptionAPIView.as_view()),
]
