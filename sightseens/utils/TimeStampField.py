import datetime
from rest_framework import serializers


class TimeStampField(serializers.Field):
    def to_native(self, value):
        epoch = datetime.datetime(1970, 1, 1)
        return int((value - epoch).total_seconds())

    # как to string
    def to_representation(self, value):
        return "%s" % value

    def to_internal_value(self, data):
        return TimeStampField(data).__str__()
