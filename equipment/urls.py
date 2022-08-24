from django.urls import path
from . import views

urlpatterns = [
    path('measureequipmentall/', views.MeasurEquipmentView.as_view(), name='measureequipmentall'),
    path('measureequipmentallsearres/', views.SearchResultMeasurEquipmentView.as_view(), name='measureequipmentallsearres'),
    path('measureequipment/<str:str>/', views.StrMeasurEquipmentView.as_view(), name='measureequipment'),
    path(r'^export/xls/$', views.export_me_xls, name='export_me_xls'),
    path('measureequipment/<str:str>/comments/', views.CommentsView.as_view(), name='measureequipmentcomm'),
    path('measureequipment/<str:str>/individuality/', views.EquipmentUpdate, name='measureequipmentind'),
    path('measureequipment/verification/<str:str>/', views.VerificationequipmentView.as_view(), name='measureequipmentver'),
    path('measureequipment/verificationreg/<str:str>/', views.VerificationReg, name='measureequipmentverificationreg'),
    path('equipmentreg/', views.EquipmentReg, name='equipmentreg'),
    path('equipmentlist/', views.EquipmentView.as_view(), name='equipmentlist'),
    path('manufacturerlist/', views.ManufacturerView.as_view(), name='manufacturerlist'),
    path('manufacturerreg/', views.ManufacturerRegView, name='manufacturerreg'),
    path('measurequipmentcharacterslist/', views.MeasurEquipmentCharaktersView.as_view(), name='measurequipmentcharacterslist'),
    path('measurequipmentcharactersreg/', views.MeasurEquipmentCharaktersRegView, name='measurequipmentcharactersreg'),
    path('measureequipmentreg/<str:str>/', views.MeasureequipmentregView.as_view(), name='measureequipmentreg'),
]
