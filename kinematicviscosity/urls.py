from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('attestation/<int:pk>/', login_required(views.StrKinematicviscosityView.as_view()), name='Str'),
    path('registration/', views.RegKinematicviscosityView, name='Reg'),
    path('attestation/', login_required(views.AllKinematicviscosityView.as_view()), name='All'),
    path('', views.AttestationJoneView.as_view(), name='kinematicviscosity'),
    path('attestation/<int:pk>/comments/', login_required(views.CommentsKinematicviscosityView.as_view()), name='comm'),
    path('filter/<int:pk>', views.viscosityobjects_filter, name="viscosityobjects_filter"),

]
