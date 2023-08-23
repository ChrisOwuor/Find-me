# from django.shortcuts import render


# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def Home(request):
    return HttpResponse("Hello, Welcome to find me web app")