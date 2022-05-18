from django.urls import path
from . import views

urlpatterns = [
    path('attestationJ/kinematicviscosity/attestation/<int:pk>/', views.ViscosityMJLView.as_view(), name='ViscosityMJLView'),
    path('attestationJ/kinematicviscosity/registration/', views.ViscosityMJLCreation, name='KVGreg'),
    path('attestationJ/kinematicviscosity/attestation/', views.ViscosityMJLAll.as_view(), name='viscosityattestationJL'),
]
