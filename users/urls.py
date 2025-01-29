from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserCreationAPIView,
    EmailVerificationAPIView,
    LoginAPIView,
    LogoutAPIView,
    ResendVerificationEmail,
    RequestPasswordResetEmail,
    PasswordResetConfirm,
    PasswordTokenCheckAPIView,
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
    path("password_reset/", RequestPasswordResetEmail.as_view(), name="password-reset"),
    path(
        "password_reset/<str:uidb64>/<str:token>/",
        PasswordTokenCheckAPIView.as_view(),
        name="reset-token-check",
    ),
    path(
        "password_reset/confirm/",
        PasswordResetConfirm.as_view(),
        name="password-reset-confirm",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("verify_email/", EmailVerificationAPIView.as_view(), name="verfiy-email"),
]
