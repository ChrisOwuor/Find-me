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

    def get(self, request):
        persons = self.new_missing_persons()
        return Response({"persons": persons})

    @classmethod
    def new_missing_persons(cls):
        """
        get all missing persons
        whose created at is same as todays date
        """

        return 20

    @classmethod
    def new_found_persons(cls):
        """
        get all found persons
        whose created at is same as todays date
        """
        ...

    @classmethod
    def user_activity(cls):
        """
        get all users created today
        whose created at is same as todays date
        """
        ...

    @classmethod
    def case_status(cls):
        """
        get all searches today
        get all pending cases today
        get all resolved cases today
        """
        ...

    @classmethod
    def model_perfomance(cls):
        """
        get all average ratings and see the performance
        """

        ...

    @classmethod
    def geographical_distribution(cls):
        """
        do geographical distribution of cases
        """
        ...


class Weekly_Activity(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        pass
