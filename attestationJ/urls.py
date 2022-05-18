from django.urls import path

from  . import views

urlpatterns = [
    path('kinematicviscosity/', views.AttestationJoneView.as_view(), name='kinematicviscosity'),
    path('dinamicviscosity/', views.AttestationJoneView2.as_view(), name='dinamicviscosity'),
]
