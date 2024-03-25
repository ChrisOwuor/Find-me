from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, OtpSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.response import Response
from .models import Otp, User
from Api.models import MissingPerson, FoundPerson
from Api.serializers import MissingPersonSerializer, ReportedSeenPersonSerializer
from django.db.models import Q


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_name'] = user.user_name
        token["email"] = user.email
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        try:
            user_instance = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"msg": "no user found"}, status=status.HTTP_404_NOT_FOUND)

        if "password" in request.data:
            return Response({"msg": "Password update not allowed"}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = CustomUserSerializer(
            data=request.data, instance=user_instance, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()

            return Response({"msg": "infromation changed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Invalid data", "errors": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        password = request.data.get('password')

        # Check if the old password is correct
        if not check_password(old_password, user.password):
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password and update the session hash
        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)

        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# view to get user details and the trackcodes


@api_view(['GET'])
def Profile(request):
    if request.method == 'GET':
        persons = User.objects.filter(user_name=request.user)
        codes = MissingPerson.objects.filter(created_by=request.user)
        codes2 = FoundPerson.objects.filter(created_by=request.user)
        serializer2 = ReportedSeenPersonSerializer(codes2, many=True)
        serializer = CustomUserSerializer(persons, many=True)
        codeserialiser = MissingPersonSerializer(codes, many=True)

        return Response({"person": serializer.data, "codes": codeserialiser.data, "codes2": serializer2.data})


class Fogortpaswd(APIView):
    permission_classes = [AllowAny]
    # sent email to see if it exists in db
    # if it exists create an otp then create an otp for the user and send the otp to user
    # then now  do a post request for the otp to verify the otp
    # if valid return true message then the frontend will use this to ether redirect you to a reset page or display an
    # input for new password

    # the new password will be the request body and then useed to update the password in the user model

    def post(self, request):
        email = request.data.get("email", "")
        if not email:
            return Response({"msg": "No email entered"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg": "No user found with the provided email"}, status=status.HTTP_404_NOT_FOUND)
        otp = Otp.objects.create(
            created_for=user,
            code=Otp.get_code()
        )
        otp_serializer = OtpSerializer(otp).data

        return Response({"code": otp_serializer["code"]})


class VerifyOtp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code", "")
        if not code:
            return Response({"msg": "No code entered"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_instance = Otp.objects.get(code=code)
        except Otp.DoesNotExist:
            return Response({"msg": "Invalid or expired OTP code"}, status=status.HTTP_404_NOT_FOUND)

        if otp_instance.is_valid():
            otp_serializer = OtpSerializer(otp_instance).data
            user = User.objects.get(id=otp_serializer.get("created_for", {}))
            user_serializer = CustomUserSerializer(user).data

            return Response({"msg": "Valid OTP. You can proceed with password change.", "user": user_serializer.get("id", "no email")})
        else:
            return Response({"msg": "Invalid or expired OTP code"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasskey(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id):

        try:
            user_instance = User.objects.get(id=id)

        except User.DoesNotExist:
            return Response({"msg": "no user found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_otp = Otp.objects.get(
                Q(created_for=user_instance.id) & Q(code=request.data.get("code")))

        except Otp.DoesNotExist:
            return Response({"msg": "Invalid data"}, status=status.HTTP_404_NOT_FOUND)

        if user_otp:
            user_serializer = CustomUserSerializer(
                data=request.data, instance=user_instance, partial=True)

            if user_serializer.is_valid():
                user_serializer.save()

                return Response({"msg": "password changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "Invalid data", "errors": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
