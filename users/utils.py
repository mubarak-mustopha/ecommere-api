from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken


class NotImplemented(BaseException):
    pass


class EmailSender:
    subject_template = "users/email_subject.txt"
    body_template = ""

    def __init__(self, request=None, domain_override=None, use_https=False):
        self.request = request
        self.domain_override = domain_override
        self.use_https = use_https

    def get_email_context(self, user):
        if not self.domain_override:
            current_site = get_current_site(self.request)
            domain = current_site.domain
            site_name = current_site.name
        else:
            domain = site_name = self.domain_override

        return {
            "email": user.email,
            "protocol": "https" if self.use_https else "http",
            "domain": domain,
            "site_name": site_name,
            "token": self.get_user_token(user),
        }

    def get_user_token(self, user):
        raise NotImplemented("Must implement get_user_token()")

    def send(self, user):
        context = self.get_email_context(user)

        subject = render_to_string(
            self.subject_template,
            context={
                "site_name": context.pop("site_name", ""),
                "title": context.pop("title", ""),
            },
        )
        message = render_to_string(self.body_template, context=context)
        email = EmailMessage(
            subject, message, from_email=settings.FROM_EMAIL, to=[user.email]
        )
        email.send()

        return user


class VerificationEmailSender(EmailSender):
    body_template = "registration/verification_email.html"

    def get_user_token(self, user):
        return str(RefreshToken.for_user(user).access_token)

    def get_email_context(self, user):
        context = super().get_email_context(user)
        context["title"] = "Activation email"

        return context


class PasswordResetEmailSender(EmailSender):
    body_template = "registration/password_reset_email.html"

    def get_user_token(self, user):
        return PasswordResetTokenGenerator().make_token(user)

    def get_email_context(self, user):
        context = super().get_email_context(user)
        context["title"] = "Password reset"
        context["uidb64"] = urlsafe_base64_encode(force_bytes(user.id))

        return context
