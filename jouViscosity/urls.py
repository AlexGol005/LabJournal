from django.urls import path

from  . import views

urlpatterns = [
    path('kinematicviscosityvalues/', views.AllKinematicviscosityView.as_view(), name='kinematicviscosityvalues'),
      ]
