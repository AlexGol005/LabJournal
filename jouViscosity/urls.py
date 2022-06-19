from django.urls import path

from  . import views

urlpatterns = [
    path('kinematicviscosityvalues/', views.AllKinematicviscosityView.as_view(), name='kinematicviscosityvalues'),
    path('kinematicаsearchresult/', views.SearchKinematicResultView.as_view(), name='kinematicаsearchresult'),
    path('detailkinematic/<path:path>/<int:int>/<str:str>', views.DetailKinematicView.as_view(), name='detailkinematic'),
    path('dinamicviscosityvalues/', views.AllDinamicviscosityView.as_view(), name='dinamicviscosityvalues'),
    path('dinamicasearchresult/', views.SearchKinematicResultView.as_view(), name='dinamicasearchresult'),
    path('detaildinamic/<path:path>/<int:int>/<str:str>', views.DetailDinamicView.as_view(), name='detaildinamic'),
      ]
