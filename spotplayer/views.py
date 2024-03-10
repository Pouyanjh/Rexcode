from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from spotplayer.paydbs.spotadd import licencecreate

@api_view(['POST'])
def addspot(request):
    data = request.data
    print(data)

    name = data['name']
    course = data['course']
    print(name)
    print(course)

    try:
        response = licencecreate(course, name)
    except:
        return Response({'detail': 'the spotplayer server connection was established !'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    resjson = response.json()
    return Response(resjson)





