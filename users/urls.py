from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserCreationAPIView,
    EmailVerificationAPIView,
    LoginAPIView,
    LogoutAPIView,
    ResendVerificationEmail,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("register/", UserCreationAPIView.as_view(), name="register"),
    path(
        "resend_verification_email/",
        ResendVerificationEmail.as_view(),
        name="resend-verification-email",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("verify_email/", EmailVerificationAPIView.as_view(), name="verfiy-email"),
]
