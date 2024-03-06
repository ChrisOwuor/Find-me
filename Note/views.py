from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny, IsAuthenticated


"""
Daily Activity Report:
Weekly/Monthly Activity Summary:
Case Status Report:
Face Recognition Performance Report:
Geographical Distribution Report:
User Activity Report:
"""


class Daily_Activity(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        persons = self.new_missing_persons()
        return Response({"persons": persons})

    @classmethod
    def new_missing_persons(cls):
        return 20

    @classmethod
    def new_found_persons(cls):
        ...

    @classmethod
    def user_activity(cls):
        ...

    @classmethod
    def case_status(cls):
        ...

    @classmethod
    def model_perfomance(cls):
        ...

    @classmethod
    def geographical_distribution(cls):
        ...


class Weekly_Activity(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        ...


class Case_Status(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        ...


class Model_Performance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        ...


class Geographical_Distribution(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        ...


class User_Activity(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        ...
