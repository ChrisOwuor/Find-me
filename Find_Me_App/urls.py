from django.urls import path
from . import views


urlpatterns = [
    path("missing-person/",views.Missing,name="missing"),
    path("find-person/<str:pid>",views.Find,name="find"),
    path("add-missing/",views.Add_Person,name="add-missing"),
    path("report-person/", views.Report_Person, name="report-person"),
]
