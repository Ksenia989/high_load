from django.db import models
from rest_framework import serializers
from sightseens.utils.TimeStampField import TimeStampField


class User(models.Model):
    """Класс, отвечающий за пользователя.
    Он может посетить много мест, быть в одном и том же в разное время с разными оценками"""

    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
    )

    '''id человека (устанавливается тестирующей системой)'''
    id = models.PositiveIntegerField(primary_key=True)
    '''электронная почта (100 символов максимум)'''
    email = models.EmailField(verbose_name="электронная почта")  # todo email also unique
    '''имя (50 символов максимум)'''
    first_name = models.CharField(max_length=50, verbose_name="имя")
    '''фамилия (50 символов максимум)'''
    last_name = models.CharField(max_length=50, verbose_name="фамилия")
    '''пол (1 символ)'''
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="пол")
    '''дата рождения в timestamp (задаётся параметром auto_now_add=True)'''
    birth_date = models.DateTimeField(auto_now_add=True, verbose_name="дата рождения")

    def __str__(self):
        return '\n id = %s,\n first_name = %s,\n last_name = %s,\n email = %s,\n gender = %s,\n birth_date = %s' % \
               (self.id, self.first_name, self.last_name, self.email, self.gender, self.birth_date)

    class Meta:
        app_label = 'sightseens'


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=1)
    birth_date = TimeStampField()
