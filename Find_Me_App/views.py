# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ReportedSeenPerson
from . import serializers
from .models import MissingPerson


# return all persons where matched is false from missing persons db
@api_view(['GET'])
def Missing(request):
    if request.method == 'GET':
        persons = MissingPerson.objects.all()
        serializer = serializers.MissingPersonSerializer(persons, many=True)
        return Response(serializer.data)


# send a post request with the id and response include not found or found including pic name location
@api_view(['GET', 'POST'])
def Find(request, pid):
    if request.method == "POST":
        print(pid)
        return Response({"pid": pid})
    elif request.method == "GET":
        person = ReportedSeenPerson.objects.get(pk=pid)
        serializer = serializers.ReportedSeenPersonSerializer(person)
        return Response(serializer.data)


# report a missing person to reported seen persons db
@csrf_exempt
@api_view(['GET', 'POST'])
def Report_Person(request):
    serializer = None
    if request.method == 'POST':

        serializer = serializers.ReportedSeenPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    elif request.method == "GET":
        person = ReportedSeenPerson.objects.all()
        serializer = serializers.ReportedSeenPersonSerializer(person, many=True)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# add missing person to missing person db
@api_view(['GET', 'POST'])
def Add_Person(request):
    serializer = None
    if request.method == 'POST':

        serializer = serializers.MissingPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=201)
    elif request.method == "GET":
        person = MissingPerson.objects.all()
        serializer = serializers.MissingPersonSerializer(person, many=True)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
