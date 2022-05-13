from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'ваш email'})
                             )
    username = forms.CharField(label='Введите логин',
                               required=True,
                               help_text='Фамилия и инициалы без пробелов',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                               'placeholder': 'ФамилияИО'}))
    # userlastname = forms.CharField(label='Фамилия',
    #                                required=True,
    #                                widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                              'placeholder': 'Фамилия'}))
    # userfirstname = forms.CharField(label='Имя', required=True,
    #                                 widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                               'placeholder': 'Имя'}))
    # userpatronymic = forms.CharField(label='Отчество',
    #                                  required=False,
    #                                  widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                'placeholder': 'Отчество'}))
    # userposition = forms.CharField(label='Должность',
    #                                required=True,
    #                                widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                              'placeholder': 'Должность'}))
    # usertelnumber = forms.CharField(label='Телефон',
    #                                required=True,
    #                                widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                              'placeholder': 'Телефон'}))
    password1 = forms.CharField(label='Введите пароль',
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                           'placeholder': 'введите пароль' }))
    password2 = forms.CharField(label='Подтвердите пароль',
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                           'placeholder': 'повторно введите пароль' }))


    class Meta:
        model = User
        # fields = ['username', 'userlastname', 'userfirstname', 'userpatronymic', 'userposition', 'email', 'usertelnumber', 'password1', 'password1' ]
        fields = ['username', 'email', 'password1', 'password1' ]