from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    url_field_name = 'id'
    url = serializers.HyperlinkedIdentityField(view_name='api:client-detail', lookup_field='id', read_only=True)

    class Meta:
        model = Client
        fields = '__all__'