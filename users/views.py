from rest_framework.request import Request
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

# from rest_framework.views import APIView


from .serializers import UserCreationSerializer, EmailVerificationSerializer

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

    def get(self, request):
        token = request.GET.get("token")

        serializer = self.serializer_class(data={"token": token})
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "Email verification successful"}, status=status.HTTP_200_OK
        )
