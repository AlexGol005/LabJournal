from django.urls import path
from . import views

urlpatterns = [
    path('measureequipmentall', views.MeasurEquipmentView.as_view(), name='measureequipmentall'),
]
