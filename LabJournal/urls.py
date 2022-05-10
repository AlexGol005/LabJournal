from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('login.urls')),
    path('', include('viscosimeters.urls')),
    path('', include('viscosityattestation.urls')),
    path('', include('users.urls')),
]
