from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('attestation/<int:pk>/', views.StrKinematicviscosityDetailView.as_view(), name='Str'),
    path('registration/', views.RegKinematicviscosityView, name='Reg'),
    path('attestation/', views.AllKinematicviscosityView.as_view(), name='All'),
    path('', views.AttestationJoneView.as_view(), name='kinematicviscosity'),
    path('attestation/<int:pk>/comments/', login_required(views.CommentsKinematicviscosityView.as_view()), name='comm'),

]
