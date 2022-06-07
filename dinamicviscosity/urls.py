from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('attestation/<int:pk>/', login_required(views.StrDinamicviscosityView.as_view()), name='str'),
    path('registration/', views.RegDinamicviscosityView, name='reg_dinamicviscosity'),
    path('attestation/', login_required(views.AllDinamicviscosityView.as_view()), name='all_dinamicviscosity'),
    path('', views.DinamicviscosityJournalView.as_view(), name='dinamicviscosity'),
    path('attestation/<int:pk>/comments/', login_required(views.CommentsKinematicviscosityView.as_view()), name='comm'),
    path('filterd/<int:pk>', views.Dinamicviscosityobjects_filter, name="filter_dinamicviscosity"),

]
