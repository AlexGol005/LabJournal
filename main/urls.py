from django.urls import path

from  . import views

urlpatterns = [
    path('hello/', views.TextHelloView.as_view(), name='hello'),
    path('', views.IndexView.as_view(), name='home'),
    path('productionJ/', views.ProductionJView.as_view(), name='prod'),
    path('attestationJ/', views.AttestationJView.as_view(), name='att')]
#     path('attestationJ/kinematicviscosity/', views.AttestationJoneView.as_view(), name='kinematicviscosity'),
#     path('attestationJ/dinamicviscosity/', views.AttestationJoneView2.as_view(), name='dinamicviscosity'),
# ]
