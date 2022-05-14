from django.urls import path, include
from . import views

urlpatterns = [
    path('viscosimeters/', views.ViscosimeterTypeView.as_view(), name='vt'),
]

