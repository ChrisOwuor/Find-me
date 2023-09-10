from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.Home,name="home"),
    path("missing-person/",views.Missing,name="missing"),
    path("find-person/",views.Find,name="find"),
    path("add-missing/",views.Add_person,name="add-missing"),
    path("found-persons/", views.Found, name="found-persons"),
    path("report-person/", views.Report_person, name="report-person")

]
