from django.urls import path
from .views import CreateNote
app_name = "Note"
urlpatterns = [
    path('notes/', CreateNote.as_view(), name="create_noter"),
]
