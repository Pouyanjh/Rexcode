from bank.models import Order
from rest_framework import serializers




class orderserializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            '_id', 'totalprice', 'paymentmethod', 'title', 'user'
        )

