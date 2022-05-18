from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.http import  HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from .models import AttestationJ

class TextHelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        text = '<h1>Hello, World</h1>'

        return HttpResponse(text)

class IndexView(View):
   def get(self, request):
       return render(request, 'main/main.html')

# @login_required
class AttestationJView(View):
   def get(self, request):
       AttestationJObjects = AttestationJ.objects.all()
       return render(request, 'main/attestationJ.html', {'AttestationJObjects': AttestationJObjects})


class ProductionJView(View):
   def get(self, request):
       return render(request, 'main/productionJ.html')

# class AttestationJoneView(View):
#     """ Представление, которое позволяет вывести отдельную запись. """
#     def get(self, request):
#         note = AttestationJ.objects.all()
#         return render(request, 'main/kinematicviscosity.html', {'note': note})
#
# class AttestationJoneView2(View):
#     """ Представление, которое позволяет вывести отдельную запись. """
#     def get(self, request):
#         note = AttestationJ.objects.all()
#         return render(request, 'main/kinematicviscosity.html', {'note': note})

