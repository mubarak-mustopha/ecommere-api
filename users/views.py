from rest_framework.request import Request
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_serializer,
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView


from .models import CustomUser
from .serializers import (
    UserCreationSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    RequestVerificationEmailSerializer,
    RequestPasswordResetEmailSerializer,
)

# Create your views here.


class UserCreationAPIView(generics.GenericAPIView):
    serializer_class = UserCreationSerializer

    def post(self, request: Request):
        # import pdb

        # pdb.set_trace()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=request, use_https=request.is_secure())

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class EmailVerificationAPIView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    @extend_schema(
        parameters=[OpenApiParameter("token", OpenApiTypes.STR, OpenApiParameter.QUERY)]
    )
    def get(self, request):
        token = request.GET.get("token")

        serializer = self.serializer_class(data={"token": token})
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "Email verification successful"}, status=status.HTTP_200_OK
        )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):

    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.data.get("token")
        RefreshToken(refresh).blacklist()
        return Response(status=status.HTTP_200_OK)


class ResendVerificationEmail(generics.GenericAPIView):

    serializer_class = RequestVerificationEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(request=request, use_https=request.is_secure())

        return Response(status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(request=request, use_https=request.is_secure())

        return Response(status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("redirect_url", OpenApiTypes.URI, OpenApiParameter.QUERY)
        ]
    )
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get("redirect_url", settings.FRONTEND_URL)

        serializer = self.serializer_class(
            data={
                "uidb64": uidb64,
                "token": token,
                "redirect_url": redirect_url,
            }
        )
        link_valid = True if serializer.is_valid() else False

        redirect_url = serializer.data["redirect_url"] + f"?link_valid={link_valid}"

        return HttpResponseRedirect(redirect_url)


class PasswordResetConfirm(generics.GenericAPIView):

    serializer_class = PasswordResetConfirmSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password reset successful"}, status=status.HTTP_200_OK
        )
