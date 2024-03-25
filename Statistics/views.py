from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, time, timedelta, datetime
from rest_framework.permissions import AllowAny, IsAuthenticated

from Api.models import FoundPerson, MissingPerson
from Api.serializers import MissingPersonSerializer, ReportedSeenPersonSerializer
from Users.models import User
from Users.serializers import CustomUserSerializer
from django.db.models import Q


"""
Daily Activity Report:
Weekly/Monthly Activity Summary:
Case Status Report:
Face Recognition Performance Report:
Geographical Distribution Report:
User Activity Report:
"""


class Daily_Activity(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, y, m, d):

        missing_persons = self.new_missing_persons(y, m, d)
        found_persons = self.new_found_persons(y, m, d)
        created_users = self.user_activity(y, m, d)
        return Response({"Missing_persons": missing_persons, "found_persons": found_persons, "accounts": created_users})

    @classmethod
    def new_missing_persons(cls, y, m, d):
        """
        get all missing persons
        whose created at is same as todays date
        """
        target_date = datetime(y, m, d)

        missing_persons = MissingPerson.objects.filter(
            created_at__date=target_date.date())
        missing_persons_serializer = MissingPersonSerializer(
            missing_persons, many=True).data

        return {"missing_persons": missing_persons_serializer, "count": missing_persons.count()}

    @classmethod
    def new_found_persons(cls, y, m, d):
        """
        get all found persons
        whose created at is same as todays date
        """
        target_date = datetime(y, m, d)

        found_persons = FoundPerson.objects.filter(
            created_at__date=target_date.date())
        found_persons_serializer = ReportedSeenPersonSerializer(
            found_persons, many=True).data

        return {"found_persons": found_persons_serializer, "count": len(found_persons_serializer)}

    @classmethod
    def user_activity(cls, y, m, d):
        target_date = datetime(y, m, d)
        """
        get all users created today
        whose created at is same as todays date
        """
        all_users = User.objects.filter(
            Q(start_date__date=target_date) & Q(is_staff=False))
        all_users_serializer = CustomUserSerializer(all_users, many=True).data
        user_details = []
        for user in all_users_serializer:

            user_details.append(
                {"email": user["email"], "user_name": user["user_name"]})

        return {"users": user_details, "total_count": len(all_users_serializer)}


class Weekly_Activity(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, y, m, d):
        missing_persons = self.new_missing_persons_range(y, m, d)
        found_persons = self.new_found_persons_range(y, m, d)
        created_users = self.user_activity_range(y, m, d)
        return Response({"Missing_persons": missing_persons, "found_persons": found_persons, "accounts": created_users})

    @classmethod
    def new_missing_persons_range(cls, y, m, d):
        """
        get all missing persons
        whose created in last six days
        """
        end_date = datetime(y, m, d)
        six_days = timedelta(days=6)
        start_date = end_date-six_days

        missing_persons = MissingPerson.objects.filter(
            created_at__date__range=[start_date.date(), end_date.date()])
        missing_persons_serializer = MissingPersonSerializer(
            missing_persons, many=True).data

        return {"missing_persons": missing_persons_serializer, "count": missing_persons.count()}

    @classmethod
    def new_found_persons_range(cls, y, m, d):
        """
        get all found persons
        whose created in last six days
        """
        end_date = datetime(y, m, d)
        six_days = timedelta(days=6)
        start_date = end_date-six_days

        found_persons = FoundPerson.objects.filter(
            created_at__date__range=[end_date.date(),start_date.date()])
        found_persons_serializer = ReportedSeenPersonSerializer(
            found_persons, many=True).data

        return {"found_persons": found_persons_serializer, "count": len(found_persons_serializer)}

    @classmethod
    def user_activity_range(cls, y, m, d):
        """
        Get all users created within a date range
        """
        end_date = datetime(y, m, d)
        six_days = timedelta(days=6)
        start_date = end_date-six_days

        all_users = User.objects.filter(
            Q(start_date__date__range=[start_date, end_date]) & Q(is_staff=False))
        all_users_serializer = CustomUserSerializer(all_users, many=True).data
        user_details = []

        for user in all_users_serializer:
            user_details.append(
                {"email": user["email"], "user_name": user["user_name"]}
            )

        return {"users": user_details, "total_count": len(all_users_serializer)}
