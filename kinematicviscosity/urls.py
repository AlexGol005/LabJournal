# все стандратно
from django.urls import path
from django.contrib.auth.decorators import login_required


from . import views
from .views import URL


urlpatterns = [
    path('', views.HeadView.as_view(), name=URL),
    path('attestation/<int:pk>/', login_required(views.StrJournalView.as_view()), name=URL + 'str'),
    path('registration/', views.RegNoteJournalView, name=URL + 'reg'),
    path('attestation/<int:pk>/comments/', login_required(views.CommentsView.as_view()), name=URL + 'comm'),
    path('attestation/', login_required(views.AllStrView.as_view()), name=URL + 'all'),
    path('searchresult/', views.SearchResultView.as_view(), name=URL + 'search'),
    path('datesearchresult/', views.DateSearchResultView.as_view(), name=URL + 'datesearch'),
    path('filter/<int:pk>', views.filterview, name=URL + 'filter'),
    path(r'^export/xls/$/<int:pk>', views.export_me_xls, name='export_kinematicviscosity_xls'),
    path(r'^export1/xls/$/<int:pk>', views.export_protocol_xls, name='export_kinematicviscosity_protocol_xls'),
    path('protocolhead/<slug:pk>', views.ProtocolHeadView.as_view(), name=URL + 'protocolhead'),
    path('protocolbutton/<slug:pk>', views.ProtocolbuttonView.as_view(), name=URL + 'protocolbutton'),

]
# path('/search_location/result/', views.SearchResultView.as_view(), name=URL + 'search'),