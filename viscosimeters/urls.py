from django.urls import path
from . import views

urlpatterns = [
    path('viscosimeterskonstants/', views.ViscosimetersView.as_view(), name='konstv'),
    path('kalibrationviscosimetersreg/', views.KalibrationViscosimetersRegView, name='kalibrationviscosimetersreg'),
    path('viscosimeters/', views.ViscosimetersHeadView.as_view(), name='vt'),
]


