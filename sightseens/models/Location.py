from django.db import models
from rest_framework import serializers


class Location(models.Model):
    """id достропримечательности (устанавливается тестирующей системой)"""  # todo 32р беззн число
    id = models.IntegerField(primary_key=True)
    '''описание достопримечательности (длина не ограничена)'''
    place = models.TextField()
    '''название страны расположения (50 символов максимум)'''
    country = models.CharField(max_length=50)
    '''название города (50 символов максимум)'''
    city = models.CharField(max_length=50)
    '''дистанция от города по прямой в километрах'''  # todo 32р беззн число
    distance = models.PositiveSmallIntegerField()

    def __str__(self):
        return '\n id = %s,\n place = %s,\n country = %s,\n city = %s,\n distance = %s' % \
               (self.id, self.place, self.country, self.city, self.distance)

    class Meta:
        app_label = 'sightseens'


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    place = serializers.CharField()
    country = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=50)
    distance = serializers.IntegerField()