from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, Fogortpaswd, MyTokenObtainPairView

from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
app_name = 'Users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profile/", views.Profile, name="profile"),
    path("profile/change/passkey/", Fogortpaswd.as_view(), name="forgot_passkey"),

]
