from django.urls import path
from . import views

urlpatterns = [
    path('viscosityattestationJL/<int:pk>', views.ViscosityMJLView.as_view(), name='vg'),
    path('KVGregister/', views.ViscosityMJLCreation, name='KVGreg'),
]
