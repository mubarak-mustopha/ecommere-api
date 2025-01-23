from django.urls import path

from .views import UserCreationAPIView, EmailVerificationAPIView

urlpatterns = [
    path("register/", UserCreationAPIView.as_view(), name="register"),
    path("verify_email/", EmailVerificationAPIView.as_view(), name="verfiy-email"),
]
