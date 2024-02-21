from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Talk
from rest_framework.decorators import api_view
from .serializer import talkserializer


@api_view(['POST'])
def talkpost(request):
    data = request.data
    talk = Talk.objects.create(
        name = data['name'],
        email = data['email'],
        description = data['description'],
    )
    serializer = talkserializer(talk, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


