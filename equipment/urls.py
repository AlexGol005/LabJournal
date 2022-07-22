from django.urls import path
from . import views

urlpatterns = [
    path('measureequipmentall/', views.MeasurEquipmentView.as_view(), name='measureequipmentall'),
    path('measureequipmentallsearres/', views.SearchResultMeasurEquipmentView.as_view(), name='measureequipmentallsearres'),
    path('measureequipment/<str:str>/', views.StrMeasurEquipmentView.as_view(), name='measureequipment' + 'pk'),
    path(r'^export/xls/$', views.export_me_xls, name='export_me_xls'),
    path('measureequipment/<str:str>/comments/', views.CommentsView.as_view(), name='measureequipmentcomm'),
    path('measureequipment/<str:str>/individuality/', views.EquipmentUpdate, name='measureequipmentind'),
    path('measureequipment/<str:str>/verification/', views.VerificationequipmentView.as_view(), name='measureequipmentver'),
]
