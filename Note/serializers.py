from rest_framework import serializers
from Note.models import Note

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ("id","user","body")
