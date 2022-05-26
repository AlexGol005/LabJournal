from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import ViscosityMJL, CommentsKinematicviscosity
from .forms import ViscosityMJLCreationForm, CommentCreationForm
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

    return render(
        request,
        'kinematicviscosity/registration.html',
        {
            'form': form
        })


class AllKinematicviscosityView(View):
    """ Представление, которое выводит все записи в журнале. """
    def get(self, request):
        viscosityobjects = ViscosityMJL.objects.order_by('-date')
        return render(request, 'kinematicviscosity/journal.html', {'viscosityobjects': viscosityobjects})


class AttestationJoneView(View):
    """ Представление, которое выводит заглавную страницу журнала """
    def get(self, request):
        note = AttestationJ.objects.all().filter(for_url='kinematicviscosity')
        return render(request, 'kinematicviscosity/head.html', {'note': note})

class CommentsKinematicviscosityView(View):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """
    form_class = CommentCreationForm
    initial = {'key': 'value'}
    template_name = 'kinematicviscosity/comments.html'
    def get(self, request, pk):
        note = CommentsKinematicviscosity.objects.filter(forNote=pk)
        title = ViscosityMJL.objects.get(pk=pk)
        form = CommentCreationForm()
        return render(request, 'kinematicviscosity/comments.html', {'note': note, 'title': title, 'form': form})
    def post(self, request, pk, *args, **kwargs):
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.forNote = ViscosityMJL.objects.get(pk=pk)
            order.save()
            # form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Комментарий добавлен!')
            return redirect(order)



    # def post(self, request):
    #     if request.method == "POST":
    #         form = CommentCreationForm(request.POST)
    #         if form.is_valid():
    #             order = form.save(commit=False)
    #             order.performer = request.user
    #             order.save()
    #             name = form.cleaned_data.get('name')
    #             messages.success(request, f'Запись об аттестации СО {name} была успешно создана!')
    #             return redirect(order)
    #     else:
    #         form = CommentCreationForm()
    #
    #     return render(
    #         request,
    #         'kinematicviscosity/comments.html',
    #         {
    #             'form': form
    #         })

# @login_required
# def CommentCreationView(request, pk):
#     if request.method == "POST":
#         form = CommentCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#
#     else:
#         form = CommentCreationForm(instance=request.   )
#
#     data = {'form': form,
#         }
#
#     return render(request, 'kinematicviscosity/comments.html', data)

# class CommentsKinematicviscosityView(View):
#     """ выводит комментарии к записи в журнале и форму для добавления комментариев """
#     form_class = CommentCreationForm
#     initial = {'key': 'value'}
#     template_name = 'kinematicviscosity/comments.html'
#
#     def get(self, reqest, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(reqest, self.template_name, {'form': form})
#
#     def post(self, reqest, *args, **kwargs):
#         form = self.form_class(reqest.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#         return  render(reqest, self.template_name, {'form': form})
#
# def CommentsKinematicviscosityView(request):
#     """ Представление, которое выводит форму регистрации в журнале. """
#     if request.method == "POST":
#         form = CommentCreationForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.performer = request.user
#             order.save()
#             # form.save()
#             name = form.cleaned_data.get('name')
#             messages.success(request, f'Запись об аттестации СО {name} была успешно создана!')
#             return redirect('comm')
#     else:
#         form = CommentCreationForm()
#
#     return render(
#         request,
#         'kinematicviscosity/comments.html',
#         {
#             'form': form
#         })