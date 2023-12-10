from django.urls import path, re_path
from . import views


app_name = "Api"

urlpatterns = [
    path("api/missing-person/", views.Missing, name="missing"),
    path("api/found-person/", views.Found, name="found"),
    path("api/find-person/<str:pid>", views.Find, name="find"),
    path("api/add-missing/", views.Add_Person, name="add-missing"),
    path("api/report-person/", views.Report_Person, name="report-person"),
    path("api/missing/details/<str:trackCode>",
         views.Missing_Details, name="fdetails"),
    path("api/seen/details/<int:id>", views.Seen_Details, name="sdetails"),
    re_path(r'^.*/?$', views.catch_all),


]
