from django.urls import path

from  . import views

urlpatterns = [
    path('chlorineoilvalues/', views.AllKinematicviscosityView.as_view(), name='chlorineoilvalues'),
    path('chlorineoilresult/', views.SearchKinematicResultView.as_view(), name='chlorineoilresult'),
    path('detailchlorineoil/<path:path>/<int:int>/<str:str>', views.DetailKinematicView.as_view(), name='detailchlorineoil'),
      ]
