import random
import string

from rest_framework import serializers
from .models import MissingPerson
from .models import ReportedSeenPerson


class MissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPerson
        fields = ("trackCode","name","age","location","description","image")

    def create(self, validated_data):
        # Generate a random trackCode
        trackCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Add the trackCode to the validated data
        validated_data['trackCode'] = trackCode

        # Call the super class's create method to save the instance to the database
        return super().create(validated_data)


class ReportedSeenPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedSeenPerson
        fields = ("name","age","description","matched","image")
