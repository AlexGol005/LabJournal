# не все стандратно
from django.urls import path
from django.contrib.auth.decorators import login_required


from . import views
from .views import URL

urlpatterns = [
    # path('dpk/<int:pk>', views.StrDPKView.as_view(), name='dpk'),
    # path('dpkreg/', views.RegDPKView, name='dpkreg'),
    # path('titranthg/<int:pk>', views.StrTitrantHgView.as_view(), name='titranthg'),
    # path('titranthgreg/', views.RegTitrantHgView, name='titranthgreg'),
    # path('gettitrhg/<int:pk>', views.StrGetTitrHgView.as_view(), name='gettitrhg'),
    # path('gettitrhgreg/', views.GetTitrHgView, name='gettitrhgreg'),
    path('', views.HeadView.as_view(), name=URL),
    # path('attestation/<int:pk>/', login_required(views.StrJournalView.as_view()), name=URL + 'str'),
    # path('registration/', views.RegNoteJournalView, name=URL + 'reg'),
    # path('attestation/<int:pk>/comments/', login_required(views.CommentsView.as_view()), name=URL + 'comm'),
    # path('attestation/', login_required(views.AllStrView.as_view()), name=URL + 'all'),
    # path('clorinesaltsallhg/', login_required(views.AllTitrantHgView.as_view()), name='allhg'),
    # path('clorinesaltsallhgtitr/', login_required(views.AllTitrantHgTitrView.as_view()), name= 'allhgtitr'),
    # path('searchresult/', views.SearchResultView.as_view(), name=URL + 'search'),
    # path('searchresultcv/', views.SearchCVResultView.as_view(), name=URL + 'searchcv'),
    # path('datesearchresult/', views.DateSearchResultView.as_view(), name=URL + 'datesearch'),
    # path('datesearchresultcv/', views.DateSearchCVResultView.as_view(), name=URL + 'datesearchcv'),
    # path('filter/<int:pk>', views.filterview, name=URL + 'filter'),
    # path('filtercv/<int:pk>', views.filtercvview, name=URL + 'filtercv'),
    # path('volumecs/', views.VolumecsView.as_view(), name='volumecs'),
    # path('clorinesaltsstrcv/<int:pk>/', login_required(views.ClorinesaltsCVView.as_view()), name='clorinesaltsstrcv'),
    # path('attestation/<int:pk>/commentscv/', login_required(views.CommentsCVView.as_view()), name=URL + 'commcv'),
    # path('attestationcv/', login_required(views.AllStrCVView.as_view()), name=URL + 'allcv'),
    # path('clorinesaltsbottles/', views.BottlesView.as_view(), name=URL + 'bottles'),
]