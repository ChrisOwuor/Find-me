# Create your views here.
import face_recognition
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .serializers import MissingPersonSerializer, ReportedSeenPersonSerializer
from .models import MissingPerson
from .models import ReportedSeenPerson
from rest_framework.parsers import MultiPartParser, FormParser
from urllib.parse import quote


# return all persons where matched is false from missing persons db
@api_view(['GET'])
def Missing(request):
    if request.method == 'GET':
        persons = MissingPerson.objects.all()
        serializer = MissingPersonSerializer(persons, many=True)
        return Response(serializer.data)


# send a post request with the id and response include not found or found including pic name location
@api_view(['GET'])
def Find(request, pid):
    if request.method == "GET":
        # Retrieve the MissingPerson instance by trackCode
        person = MissingPerson.objects.get(trackCode=pid)
        serializer = MissingPersonSerializer(person)

        # Load the image and encode the face
        img_path = "." + serializer.data["image"]
        image = face_recognition.load_image_file(img_path)
        image_encodings = face_recognition.face_encodings(image)

        # Retrieve and filter the ReportedSeenPerson instances (adjust the filter criteria)
        found_persons = ReportedSeenPerson.objects.all()
        serializer = ReportedSeenPersonSerializer(found_persons, many=True)
        found_persons_array = serializer.data

        matches = []

        for found_person in found_persons_array:
            fimg_path = "." + found_person["image"]
            fimage = face_recognition.load_image_file(fimg_path)
            fimage_encodings = face_recognition.face_encodings(fimage)

            # Check if there are any face encodings in the list
            if len(fimage_encodings) > 0:
                # Compare the encodings using compare_faces
                results = face_recognition.compare_faces(image_encodings[0], fimage_encodings)
                if results[0]:
                    matches.append({"name":found_person["name"],"image":found_person["image"]})
                print(results)

                # Append the result to the matches list

        return Response(matches)


# report a missing person to reported seen persons db
@api_view(['POST'])
def Report_Person(request):
    if request.method == 'POST':

        serializer = ReportedSeenPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "thank you for successfully adding a missing person"}, status=201)


# add missing person to missing person db
@parser_classes([MultiPartParser, FormParser])
@api_view(['POST'])
def Add_Person(request):
    if request.method == 'POST':
        serializer = MissingPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
    else:
        print('error', MissingPersonSerializer.errors)
        return Response(MissingPersonSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
