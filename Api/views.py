# Create your views here.


from django.shortcuts import render  # Import json module
from .models import MissingPerson, ReportedSeenPerson
import face_recognition
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from .serializers import MissingPersonSerializer, ReportedSeenPersonSerializer
from .models import MissingPerson
from .models import ReportedSeenPerson
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


def catch_all(request):
    return render(request, "index.html")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Profile(request):
    if request.method == 'GET':
        persons = MissingPerson.objects.filter(user_name=request.user)
        serializer = MissingPersonSerializer(persons, many=True)

        return Response(serializer.data)


# view to get all  missing persons
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Missing(request):
    if request.method == 'GET':
        # Filter missing persons by the currently authenticated user
        # persons = MissingPerson.objects.filter(created_by=request.user)
        persons = MissingPerson.objects.all()

        # Create a list to store serialized data with user names
        serialized_data = []

        for person in persons:
            data = MissingPersonSerializer(person).data
            # Replace 'user_name' with the actual field name for the user's name
            data['created_by'] = person.created_by.user_name
            serialized_data.append(data)

        return Response(serialized_data)

# view to serve a single missing person using the trackCode


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Details(request, trackCode):
    if request.method == 'GET':
        # Filter missing persons by the currently authenticated user
        persons = MissingPerson.objects.filter(trackCode=trackCode)

        # Create a list to store serialized data with user names
        serialized_data = []

        for person in persons:
            data = MissingPersonSerializer(person).data
            # Replace 'user_name' with the actual field name for the user's name
            data['created_by'] = person.created_by.user_name
            serialized_data.append(data)

        return Response(serialized_data)
# send a post request with the id and response include not found or found including pic name location

# view to do the facial recognition part


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
                results = face_recognition.compare_faces(
                    image_encodings[0], fimage_encodings)
                if results[0]:
                    matches.append({"name": found_person["first_name"],
                                   "age": found_person["age"]})
                print(results)

                # Append the result to the matches list

        return Response(matches)


# view to report a missing person to reported seen persons db
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def Report_Person(request):
    if request.method == 'POST':
        request.data['created_by'] = request.user.id
        serializer = ReportedSeenPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "thank you for successfully adding a missing person"}, status=201)


# view to add missing person to missing person db
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def Add_Person(request):
    if request.method == 'POST':
        request.data['created_by'] = request.user.id
        serializer = MissingPersonSerializer(data=request.data)
        if serializer.is_valid():

            return Response(serializer.data, status=201)

    else:
        print('error', MissingPersonSerializer.errors)
        return Response(MissingPersonSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



















