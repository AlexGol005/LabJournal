from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name= 'Логин сотрудника')
    img = models.ImageField('фото сотрудника', default='default.png', upload_to='user_images')

    def __str__(self):
        return f'Профиль сотрудника {self.user.username}'

    class Meta:
        verbose_name = 'Профиль сотрудника'
        verbose_name_plural = 'Профили сотрудников'
