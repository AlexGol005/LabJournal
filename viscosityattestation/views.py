from django.shortcuts import render
from django.http import HttpResponse
from .models import ViscosityMJL
from django.shortcuts import get_object_or_404
from django.views import View


class ViscosityMJLView(View):
    """ Представление, которое позволяет вывести отдельную запись. """
    def get(self, request, pk):
        note = get_object_or_404(ViscosityMJL, pk=pk)
        return render(request, 'viscosityattestation/vg_n.html', {'note': note})

