from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUdateForm, ProfileUdateForm
from django.contrib import messages
from django.contrib.auth.decorators import  login_required


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользовать {username} был успешно создан!')
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(
        request,
        'users/registration.html',
        {
            'title': 'Страница регистрации',
            'form': form
        } )

@login_required
def profile(request):
    if request.method == "POST":
        profailForm = ProfileUdateForm(request.POST, request.FILES,  instance=request.user.profile)
        userUpdadeForm = UserUdateForm(request.POST, instance=request.user)
        if profailForm.is_valid() and userUpdadeForm.is_valid():
            profailForm.save()
            userUpdadeForm.save()
            messages.success(request, f'данные были успешно обновлены')
            return redirect('profile')

    else:
        profailForm = ProfileUdateForm(instance=request.user.profile)
        userUpdadeForm = UserUdateForm(instance=request.user)

    data = {'profailForm': profailForm,
            'userUpdadeForm': userUpdadeForm
            }

    return render(request, 'users/profile.html', data)

