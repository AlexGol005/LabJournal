from django.urls import path, include
from . import views

urlpatterns = [
    path('viscosityattestationJL/<int:pk>', views.ViscosityMJLView.as_view(), name='vg'),
]

