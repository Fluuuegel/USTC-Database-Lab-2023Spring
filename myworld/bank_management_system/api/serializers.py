from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = '__all__'