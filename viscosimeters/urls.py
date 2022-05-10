from django.urls import path, include
from . import views

urlpatterns = [
    path('viscosimeters/', views.viscosimeters_list),
]

