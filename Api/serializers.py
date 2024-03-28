from rest_framework import serializers
from .models import MissingPerson, FoundPerson, FoundPersonLocation, MissingPersonLocation


class MissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPerson
        fields = '__all__'


class ReportedSeenPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundPerson
        fields = '__all__'


class FoundPersonLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundPersonLocation
        fields = '__all__'


class MissingPersonLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPersonLocation
        fields = '__all__'
