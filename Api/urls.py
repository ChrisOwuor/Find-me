from django.urls import path, re_path
from . import views


app_name = "Api"

urlpatterns = [
    path("api/missing-person/", views.Missing, name="missing"),
    path("api/find-person/<str:pid>", views.Find, name="find"),
    path("api/add-missing/", views.Add_Person, name="add-missing"),
    path("api/report-person/", views.Report_Person, name="report-person"),
    path("api/details/<str:trackCode>", views.Details, name="details"),
    path("api/profile/", views.Profile, name="profile"),
    re_path(r'^.*/?$', views.catch_all),


]
