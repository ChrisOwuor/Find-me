
from .models import ReportedSeenPerson


from rest_framework import serializers
import random
import string
from rest_framework import serializers
from .models import MissingPerson

class MissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPerson
        fields = ['id','created_by', 'trackCode', 'first_name', 'middle_name', 'last_name', 'nick_name', 'county', 'last_seen', 'eye_color', 'hair_color', 'age', 'location', 'description', 'image', 'gender', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Generate a unique trackCode
        while True:
            trackCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not MissingPerson.objects.filter(trackCode=trackCode).exists():
                break

        # Add the trackCode to the validated data
        validated_data['trackCode'] = trackCode

        # Call the super class's create method to save the instance to the database
        return super().create(validated_data)



class ReportedSeenPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedSeenPerson
        fields = ['id','created_by', 'first_name', 'middle_name', 'county', 'last_seen', 'eye_color', 'hair_color', 'age', 'location', 'description', 'image', 'gender', 'created_at', 'updated_at']
