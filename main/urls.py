from django.urls import path

from  . import views

urlpatterns = [
    path('hello/', views.TextHelloView.as_view()),
    path('', views.IndexView.as_view()),

]