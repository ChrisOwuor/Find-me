from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import NewUser
from Api.models import MissingPerson, ReportedSeenPerson
from Api.serializers import MissingPersonSerializer, ReportedSeenPersonSerializer


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
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        persons = NewUser.objects.filter(user_name=request.user)
        codes = MissingPerson.objects.filter(created_by=request.user)
        codes2 = ReportedSeenPerson.objects.filter(created_by=request.user)
        serializer2 = ReportedSeenPersonSerializer(codes2, many=True)
        serializer = CustomUserSerializer(persons, many=True)
        codeserialiser = MissingPersonSerializer(codes, many=True)
        print(serializer.data)
        print(codeserialiser.data)

        return Response({"person": serializer.data, "codes": codeserialiser.data, "codes2": serializer2.data})
