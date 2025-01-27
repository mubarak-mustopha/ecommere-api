import jwt

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpRequest
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, TokenBackendError

from .models import CustomUser
from .utils import VerificationEmailSender


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=68)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def save(self, **kwargs):
        user = CustomUser.objects.create_user(**self.validated_data)
        VerificationEmailSender(**kwargs).send(user)

        return user


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        token = attrs.get("token")
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM]
            )
            user = CustomUser.objects.get(id=payload["user_id"])
            user.is_verified = True
            user.save()
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Expired token provided")
        except:
            raise serializers.ValidationError("Token is invalid")
        return attrs


class VerificationEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        fields = ["email"]

    def save(self, **kwargs):
        email = self.validated_data.get("email")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                f"No user associated with the email `{email}`"
            )

        VerificationEmailSender(**kwargs).send(user)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "tokens"]

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user: CustomUser = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Incorrect credentials provided")
        if not user.is_verified:
            raise serializers.ValidationError("Email is yet to be verified.")
        return {
            "email": email,
            "tokens": user.tokens,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        fields = ["refresh"]

    def validate_refresh(self, value):
        try:
            return str(RefreshToken(value))
        except (TokenBackendError, TokenError):
            raise serializers.ValidationError(
                "Refresh token is invalid or already blacklisted."
            )
