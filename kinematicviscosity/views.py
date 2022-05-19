from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import ViscosityMJL
from .forms import ViscosityMJLCreationForm
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import AttestationJ


class StrKinematicviscosityView(View):
    """ Представление, которое позволяет вывести отдельную запись. """
    def get(self, request, pk):
        note = get_object_or_404(ViscosityMJL, pk=pk)
        return render(request, 'kinematicviscosity/str.html', {'note': note})

@login_required
def RegKinematicviscosityView(request):
    """ Представление, которое выводит форму регистрации в журнале. """
    if request.method == "POST":
        form = ViscosityMJLCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            # form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Запись об аттестации СО {name} была успешно создана!')
            return redirect(order)
    else:
        form = ViscosityMJLCreationForm()

    def get_success_url(self):
        # Вот в этом методе у вас доступен self.object.id
        return reverse('home')

    return render(
        request,
        'kinematicviscosity/registration.html',
        {
            'form': form
        })


class AllKinematicviscosityView(View):
    """ Представление, которое выводит все записи в журнале. """
    def get(self, request):
        viscosityobjects = ViscosityMJL.objects.all()
        return render(request, 'kinematicviscosity/journal.html', {'viscosityobjects': viscosityobjects})


class AttestationJoneView(View):
    """ Представление, которое выводит заглавную страницу журнала """
    def get(self, request):
        note = AttestationJ.objects.all().filter(for_url='kinematicviscosity')
        return render(request, 'kinematicviscosity/head.html', {'note': note})