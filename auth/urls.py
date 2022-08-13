from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth.api.views import RegisterView

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="user_register"),
]
