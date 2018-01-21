from django.db import models
from rest_framework import serializers

from sightseens.models.User import User
from sightseens.models.Location import Location
from sightseens.utils.TimeStampField import TimeStampField


class Visit(models.Model):
    from djchoices import DjangoChoices

    class Mark(DjangoChoices):
        from djchoices import ChoiceItem

        one = ChoiceItem(1)
        two = ChoiceItem(2)
        three = ChoiceItem(3)
        four = ChoiceItem(4)
        five = ChoiceItem(5)

    '''id посещения (устанавливается тестирующей системой)'''
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    '''id достопримечательности'''
    location = models.ForeignKey(Location, related_name="location", on_delete=models.CASCADE)  # todo cascale ли
    '''id путешественника'''
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    '''дата посещения в timestamp (задаётся параметром auto_now_add=True)'''
    visited_at = models.DateTimeField(auto_now_add=True)
    '''оценка 1 .. 5'''
    mark = models.PositiveSmallIntegerField(choices=Mark.choices)

    def __str__(self):
        return 'Sigthseen is: %s, located in %s, user is %s, he visited it in %s, mark is %s' % (
            self.id, self.location, self.user, self.visited_at, self.mark)

    class Meta:
        app_label = 'sightseens'



class VisitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    location = serializers.SlugRelatedField(slug_field='id', many=False, read_only=True)
    user = serializers.SlugRelatedField(slug_field='id', many=False, read_only=True)
    visited_at = TimeStampField()
    mark = serializers.IntegerField()

    def create(self, data):
        global u
        # что за магия????
        try:
            u=User.objects.get(pk=data['user'])
        except Exception:
            u = User.objects.get(pk=data['user'].id)
        data["user"] = u
        try:
            data["location"] = Location.objects.get(pk=data['location'])
        except Exception:
            data["location"] = Location.objects.get(pk=data['location'].id)
        return Visit.objects.create(**data)


class PlaceSerializer(serializers.Serializer):
    place = serializers.CharField()


class ShortVisitSerializer(serializers.HyperlinkedModelSerializer):
    mark = serializers.IntegerField()
    visited_at = TimeStampField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(ShortVisitSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Visit
        fields = ('mark', 'visited_at')

    def perform_create(self, serializer):
        mark = serializers.IntegerField()
        visited_at = TimeStampField()
        # todo что такое 55
        serializer.save(place='55')
