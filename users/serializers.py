import jwt

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpRequest
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=68)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def save(self, **kwargs):
        user = CustomUser.objects.create_user(**self.validated_data)
        email_context = self.get_email_context(user, **kwargs)

        subject = render_to_string(
            "users/email_subject.txt",
            context={"site_name": email_context.pop("site_name", None)},
        )
        message = render_to_string(
            "registration/verification_email.html", context=email_context
        )
        email = EmailMessage(
            subject, message, from_email=settings.FROM_EMAIL, to=[user.email]
        )
        email.send()

        return user

    def get_email_context(
        self, user, request=None, domain_override=None, use_https=False, **kwargs
    ):
        if not domain_override:
            current_site = get_current_site(request)
            domain = current_site.domain
            site_name = current_site.name
        else:
            domain = site_name = domain_override

        return {
            "email": user.email,
            "protocol": "https" if use_https else "http",
            "domain": domain,
            "site_name": site_name,
            "token": str(RefreshToken.for_user(user).access_token),
        }


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=8)

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
