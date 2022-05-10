from django.urls import path, include
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('register/', views.register, name='reg'),
    path('login/', authViews.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit')
]

