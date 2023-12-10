from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import  NoteSerializer
from .models import Note
from rest_framework.permissions import AllowAny
# Create your views here.
class CreateNote(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save()
            if note:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        note = Note.objects.all()
        serializer = NoteSerializer(note, many=True)
        json = serializer.data
        return Response(json, status=status.HTTP_302_FOUND)
