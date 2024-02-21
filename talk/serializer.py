from rest_framework import serializers
from .models import Talk




class talkserializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = (
            'name', 'email', 'description'
        )
