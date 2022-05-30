from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('kinematicviscosity/attestation/<int:pk>/', views.StrKinematicviscosityDetailView.as_view(), name='Str'),
    path('kinematicviscosity/registration/', views.RegKinematicviscosityView, name='Reg'),
    path('kinematicviscosity/attestation/', views.AllKinematicviscosityView.as_view(), name='All'),
    path('kinematicviscosity/', views.AttestationJoneView.as_view(), name='kinematicviscosity'),
    path('kinematicviscosity/attestation/<int:pk>/comments/', login_required(views.CommentsKinematicviscosityView.as_view()), name='comm'),

]
