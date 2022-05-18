from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.http import  HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from main.models import AttestationJ



class AttestationJoneView(View):
    """ Представление, которое позволяет вывести отдельную запись. """
    def get(self, request):
        note = AttestationJ.objects.all().filter(for_url='kinematicviscosity')
        return render(request, 'attestationJ/kinematicviscosity.html', {'note': note})



class AttestationJoneView2(View):
    """ Представление, которое позволяет вывести отдельную запись. """
    def get(self, request):
        note = AttestationJ.objects.all().filter(for_url='dinamicviscosity')
        return render(request, 'attestationJ/dinamicviscosity.html', {'note': note})




