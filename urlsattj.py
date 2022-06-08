from django.urls import path
from django.contrib.auth.decorators import login_required


from kinematicviscosity import views
from kinematicviscosity.views import URL


urlpatterns = [
    path('', views.HeadView.as_view(), name=URL),
#     path('attestation/<int:pk>/', login_required(views.StrJournalView.as_view()), name=URL + 'str'),
#     path('registration/', views.RegNoteJournalView, name=URL + 'reg'),
#     path('attestation/<int:pk>/comments/', login_required(views.CommentsView.as_view()), name=URL + 'comm'),
#     path('attestation/', login_required(views.AllStrView.as_view()), name=URL + 'all'),
#     path('filter/<int:pk>', views.filterview, name=URL + 'filter'),
]
