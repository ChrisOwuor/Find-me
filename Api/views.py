

from rest_framework.decorators import api_view, permission_classes
from Statistics.models import Case
from Statistics.serializers import CaseSerializer
from .models import MissingPerson, FoundPerson
import face_recognition
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from .serializers import MissingPersonSerializer, ReportedSeenPersonSerializer
from .models import MissingPerson
from .models import FoundPerson
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated



# view to get all  missing persons
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Missing(request):
    if request.method == 'GET':

        persons = MissingPerson.objects.all()

        serialized_data = []
        # print(request.user)

        for person in persons:
            data = MissingPersonSerializer(person).data

            data['created_by'] = person.created_by.user_name
            serialized_data.append(data)

        return Response(serialized_data)


# view to get all  found persons
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Found(request):
    if request.method == "GET":

        persons = FoundPerson.objects.all()

        serialized_data = []

        for person in persons:
            data = ReportedSeenPersonSerializer(person).data

            data['created_by'] = person.created_by.user_name
            serialized_data.append(data)

        return Response(serialized_data)


# view to serve a single seen person using the id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Seen_Details(request, id):
    if request.method == 'GET':

        persons = FoundPerson.objects.filter(id=id)

        serialized_data = []

        for person in persons:
            data = ReportedSeenPersonSerializer(person).data

            data['created_by'] = person.created_by.user_name
            serialized_data.append(data)

        return Response(serialized_data)

# view to serve a single missing person using the trackCode


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Missing_Details(request, trackCode):
    if request.method == 'GET':

        persons = MissingPerson.objects.filter(trackCode=trackCode)

        serialized_data = []

        for person in persons:
            data = MissingPersonSerializer(person).data

            data['created_by'] = person.created_by.user_name
            serialized_data.append(data)

        return Response(serialized_data)
# send a post request with the id and response include not found or found including pic name location

# view to do the facial recognition part


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Find(request, pid):

    if request.method == "GET":
        data = []

        person = MissingPerson.objects.get(trackCode=pid)
        serializer = MissingPersonSerializer(person)
        data.append(serializer.data)

        img_path = "." + serializer.data["image"]
        image = face_recognition.load_image_file(img_path)
        image_encodings = face_recognition.face_encodings(image)

        found_persons = FoundPerson.objects.all()
        serializer = ReportedSeenPersonSerializer(found_persons, many=True)
        found_persons_array = serializer.data

        matches = []

        for found_person in found_persons_array:
            fimg_path = "." + found_person["image"]
            fimage = face_recognition.load_image_file(fimg_path)
            fimage_encodings = face_recognition.face_encodings(fimage)

            if len(fimage_encodings) > 0:
                results = face_recognition.compare_faces(
                    image_encodings[0], fimage_encodings)
                if results[0]:
                    matches.append({"name": found_person["first_name"],
                                    "id": found_person["id"],
                                    "image": found_person["image"],
                                   "age": found_person["age"]})
                print(results)

        return Response({"matches": matches, "mps": data})

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


# view to add missing person to missing person db and create them a case
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def Add_Person(request):
    if request.method == 'POST':
        request.data['created_by'] = request.user.id
        serializer = MissingPersonSerializer(data=request.data)

        if serializer.is_valid():
            missing_person = serializer.save()

            case_data = {'missing_person': missing_person.id}
            case_serializer = CaseSerializer(data=case_data)

            if case_serializer.is_valid():
                new_case = case_serializer.save()

                # Serialize the MissingPerson instance
                missing_person_serializer = MissingPersonSerializer(
                    missing_person).data

                new_case_serializer = CaseSerializer(new_case).data

                return Response({
                    'missing_person': missing_person_serializer,
                    'case': new_case_serializer
                }, status=201)

    return Response(serializer.errors, status=400)
