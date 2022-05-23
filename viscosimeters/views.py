from django.shortcuts import render
from django.views import View
from django.http import  HttpResponse, HttpRequest
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ViscosimeterType, Viscosimeters
from .forms import ViscosimetersCreationForm


# def ViscosimeterTypeView(request):
#     ViscosimeterTypeObjects = ViscosimeterType.objects.all()
#     return render(request, 'viscosimeters/viscosimeterType.html', {'ViscosimeterTypeObjects': ViscosimeterTypeObjects})


class ViscosimeterTypeView(View):

    def get(self, request):
        ViscosimeterTypeObjects = ViscosimeterType.objects.order_by('viscosimeterType__diameter')
        return render(request, 'viscosimeters/viscosimeterType.html', {'ViscosimeterTypeObjects': ViscosimeterTypeObjects})

class ViscosimetersKonstantsView(View):
    '''должна выводить список вискозиметров с актуальными константами'''
    def get(self, request):
        ViscosimetersObjects = Viscosimeters.objects.order_by('viscosimeterType_id')
        return render(request, 'viscosimeters/viscosimetersKonstants.html', {'ViscosimetersObjects': ViscosimetersObjects})


@login_required
def viscosimetersRegView(request):
    """ выводит форму внесения вискозиметров. """
    if request.method == "POST":
        form = ViscosimetersCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            # form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Запись была успешно создана!')
            return redirect('/attestationJ/kinematicviscosity/')
    else:
        form = ViscosimetersCreationForm()

    return render(
        request,
        'viscosimeters/registration.html',
        {
            'form': form
        })



