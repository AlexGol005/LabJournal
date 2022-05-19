from django.urls import path
from . import views

urlpatterns = [
    path('attestationJ/kinematicviscosity/attestation/<int:pk>/', views.StrKinematicviscosityView.as_view(), name='StrKinematicviscosity'),
    path('attestationJ/kinematicviscosity/registration/', views.RegKinematicviscosityView, name='RegKinematicviscosity'),
    path('attestationJ/kinematicviscosity/attestation/', views.AllKinematicviscosityView.as_view(), name='AllKinematicviscosity'),
    path('attestationJ/kinematicviscosity/', views.AttestationJoneView.as_view(), name='kinematicviscosity'),
]
