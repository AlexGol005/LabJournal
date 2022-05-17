from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import ViscosityMJL
from .forms import ViscosityMJLCreationForm
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class ViscosityMJLView(View):
    """ Представление, которое позволяет вывести отдельную запись. """
    def get(self, request, pk):
        note = get_object_or_404(ViscosityMJL, pk=pk)
        return render(request, 'viscosityattestation/vg_n.html', {'note': note})

@login_required
def ViscosityMJLCreation(request):
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
        'viscosityattestation/registration.html',
        {
            'form': form
        })


class ViscosityMJLAll(View):

    def get(self, request):
        ViscosityMJLObjects = ViscosityMJL.objects.all()
        return render(request, 'viscosityattestation/all_obj_kvg.html', {'ViscosityMJLObjects': ViscosityMJLObjects})
