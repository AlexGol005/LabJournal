from django.urls import path, include
from . import views

urlpatterns = [
    path('viscosimetersType/', views.ViscosimeterTypeView.as_view(), name='viscosimetersType'),
    path('viscosimeterskonstants/', views.ViscosimetersView.as_view(), name='konstv'),
    path('kalibrationviscosimetersreg/', views.KalibrationViscosimetersRegView, name='kalibrationviscosimetersreg'),
    path('viscosimeters/', views.ViscosimetersHeadView.as_view(), name='vt'),
    path(r'^export/xls/$', views.export_users_xls, name='export_users_xls'),
]


