from django.urls import path

from  . import views

urlpatterns = [
    path('kinematicviscosityvalues/', views.AllKinematicviscosityView.as_view(), name='kinematicviscosityvalues'),
    path('dinamicviscosityvalues/', views.AllDinamicviscosityView.as_view(), name='dinamicviscosityvalues'),
      ]
