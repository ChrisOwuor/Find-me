
from .models import FoundPerson
from rest_framework import serializers
import random
import string
from rest_framework import serializers
from .models import MissingPerson


class MissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPerson
        fields = ['id',  'created_by', 'trackCode', 'first_name', 'middle_name', 'last_name', 'nick_name', 'county', 'last_seen',
                  'eye_color', 'hair_color', 'age', 'location', 'description', 'image', 'gender', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Create a new Client instance linked to the user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class ReportedSeenPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundPerson
        fields = ['id', 'created_by', 'first_name', 'middle_name', 'last_name', 'county', 'last_seen', 'eye_color',
                  'hair_color', 'age', 'location', 'description', 'image', 'gender', 'created_at', 'updated_at']
