# Create your views here.
from django.http import HttpResponse


# return all persons from db name and status with images
def Home(request):
    return HttpResponse("Hello, Welcome to find me web app")


# return all persons where matched is false
def Missing(request):
    return HttpResponse("Welcome to missing persons here i will provide you with all data for missing persons")


# return all persons where matched is true
def Found(request):
    return HttpResponse("Welcome to Found persons page")


# send a post request with the id and response include not found or found including pic name location
def Find(request):
    return HttpResponse("Here you will search fro a missing person")


# add a missing person
def Add_person(request):
    return HttpResponse("add a missing person")


# report  seen person
def Report_person(request):
    return HttpResponse("here you will report a seen person")
