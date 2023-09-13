from rest_framework import serializers
from .models import MissingPerson
from .models import ReportedSeenPerson


class MissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPerson
        fields = '__all__'


class ReportedSeenPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedSeenPerson
        fields = '__all__'
