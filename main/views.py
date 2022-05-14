from django.shortcuts import render
from django.views import View
from django.http import  HttpResponse, HttpRequest

class TextHelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        text = '<h1>Hello, World</h1>'

        return HttpResponse(text)

class IndexView(View):
   def get(self, request):
       return render(request, 'main/main.html')

class AttestationJView(View):
   def get(self, request):
       return render(request, 'main/attestationJ.html')

class ProductionJView(View):
   def get(self, request):
       return render(request, 'main/productionJ.html')