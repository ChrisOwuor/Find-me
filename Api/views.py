from rest_framework.decorators import api_view, permission_classes
from Statistics.serializers import CaseSerializer
from .models import MissingPerson, FoundPerson, MissingPersonLocation
import face_recognition
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from .serializers import FoundPersonLocationSerializer, MissingPersonLocationSerializer, MissingPersonSerializer, ReportedSeenPersonSerializer
from .models import MissingPerson
from .models import FoundPerson
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
        try:
            # Extract data from the request
            first_name = request.data.get('first_name')
            middle_name = request.data.get('middle_name')
            last_name = request.data.get('last_name')
            eye_color = request.data.get('eye_color')
            hair_color = request.data.get('hair_color')
            age = request.data.get('age')
            description = request.data.get('description')
            gender = request.data.get('gender')
            nick_name = request.data.get('nick_name')
            image = request.data.get('image')

            # Prepare data for serialization
            found_person_data = {
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'eye_color': eye_color,
                'hair_color': hair_color,
                'age': age,
                'description': description,
                'nick_name': nick_name,
                'image': image,
                'gender': gender,
                'created_by': request.user.id
            }

            # Serialize found person data
            serializer = ReportedSeenPersonSerializer(data=found_person_data)
            if serializer.is_valid():
                found_person = serializer.save()

                # Extract location data
                county = request.data.get('county')
                name = request.data.get('name')
                latitude = request.data.get('latitude')
                longitude = request.data.get('longitude')
                time_found = request.data.get('time_found')

                # Prepare location data for serialization
                found_person_location_data = {
                    'county': county,
                    'name': name,
                    'latitude': latitude,
                    'longitude': longitude,
                    'time_found': time_found,
                    'found_person': found_person.id
                }

                # Serialize location data
                seen_person_serializer = FoundPersonLocationSerializer(
                    data=found_person_location_data)
                if seen_person_serializer.is_valid():
                    seen_person_serializer.save()
                    return Response({"message": "Thank you for successfully adding a missing person"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Failed to add location data", "details": seen_person_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Failed to add found person data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# view to add missing person to missing person db and create them a case
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def Add_Person(request):
    if request.method == 'POST':
        try:
            missing_person_data = {}
            for field in MissingPerson._meta.fields:
                field_name = field.name
                if field_name in request.data:
                    missing_person_data[field_name] = request.data[field_name]

            # Set the 'created_by' field to the current user
            missing_person_data['created_by'] = request.user.id

            # Save the missing person
            missing_person_serializer = MissingPersonSerializer(
                data=missing_person_data)
            if missing_person_serializer.is_valid():
                missing_person = missing_person_serializer.save()

                # Create a case for the missing person
                case_data = {'missing_person': missing_person.id}
                case_serializer = CaseSerializer(data=case_data)

                if case_serializer.is_valid():
                    new_case = case_serializer.save()

                    # Add location details for the missing person
                    location_data = {}
                    for field in MissingPersonLocation._meta.fields:
                        field_name = field.name
                        if field_name in request.data:
                            location_data[field_name] = request.data[field_name]

                    # Set the missing person for the location
                    location_data['missing_person'] = missing_person.id

                    # Save the location details
                    location_serializer = MissingPersonLocationSerializer(
                        data=location_data)
                    if location_serializer.is_valid():
                        location_serializer.save()
                    else:
                        return Response({"error": "Failed to add location details", "details": location_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Failed to create a case", "details": case_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Failed to add missing person", "details": missing_person_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Missing person added successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
