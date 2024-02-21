
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import Http404
from django.shortcuts import redirect
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import user
import uuid
from .serializer import RegisterSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username,
        token['email'] = user.email,
        token['id'] = user.id,
        # ...

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_email_verified:
            raise serializers.ValidationError(
                {"auth error": "Please verify your email address."}
            )

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = user.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        uid = str(uuid.uuid4())
        user.activation_key = uid
        user.save()


        subject, from_email = "لطقا ایمیل را تایید کنید", "info@rexcode.ir"
        to = [user.email]
        text_content = "This is an important message."
        html_content = f"<h1>درود خوش آمدید به سایت رکس کد لطقا برای احراز هویت بر روی لینک زیر کلیک بفرمایید با تشکر </h1><a href='http://127.0.0.1:8000/account-verify/{uid}' style= 'padding: 5px; background-color: azure;  text-align: center; text-decoration: none; font-size: 30px;'>کلیک کنید </a> "
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class VerifyEmail(APIView):
    def get(self, request, uid):
        User = None  # define the User object before using it in try block
        try:
            User = user.objects.get(activation_key=uid)
            User.is_email_verified = True
            User.activation_key = ''
            User.save()
            return redirect('http://rexcode.ir')

        except user.DoesNotExist:
            return Response({'message': 'Invalid activation link'}, status.HTTP_400_BAD_REQUEST)


