from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField('Фото сотрудника', default='user_images/default.png', upload_to='user_images')
    userlastname = models.CharField('Фамилия', max_length=50, default=None, null=True)
                                   # required=True,
                                   # widget=models.TextInput(attrs={'class': 'form-control',
                                   #                               'placeholder': 'Фамилия'}))
    userfirstname = models.CharField('Имя', max_length=50, default=None, null=True)
                                    #  required=True,
                                    # widget=models.TextInput(attrs={'class': 'form-control',
                                    #                               'placeholder': 'Имя'}))
    userpatronymic = models.CharField('Отчество', max_length=50, default=None, null=True)
                                     # required=False,
                                     # widget=models.TextInput(attrs={'class': 'form-control',
                                     #                               'placeholder': 'Отчество'}))
    userposition = models.CharField('Должность', max_length=50, default=None, null=True)
                                   # required=True,
                                   # widget=models.TextInput(attrs={'class': 'form-control',
                                   #                               'placeholder': 'Должность'}))
    usertelnumber = models.CharField('Телефон', max_length=50, default=None, null=True)
                                   # required=True,
                                   # widget=models.TextInput(attrs={'class': 'form-control',
                                   #                               'placeholder': 'Телефон'}))

    def __str__(self):
        return f'Профиль сотрудника {self.user.username}'

    class Meta:
        verbose_name = 'Профиль сотрудника'
        verbose_name_plural = 'Профили сотрудников'
