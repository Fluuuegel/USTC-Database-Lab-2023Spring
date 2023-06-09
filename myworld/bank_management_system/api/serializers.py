from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    url_field_name = 'id'
    url = serializers.HyperlinkedIdentityField(view_name='api:staff-detail', lookup_field='id', read_only=True)

    class Meta:
        model = Staff
        fields = '__all__'
        
class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    url_field_name = 'id'
    url = serializers.HyperlinkedIdentityField(view_name='api:loan-detail', lookup_field='id', read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'

class Client_LoanSerializer(serializers.ModelSerializer):
    url_field_name = 'id'
    url = serializers.HyperlinkedIdentityField(view_name='api:client_loan-detail', lookup_field='id', read_only=True)

    class Meta:
        model = Client_Loan
        fields = '__all__'

class Client_BranchSerializer(serializers.ModelSerializer):
    url_field_name = 'id'
    url = serializers.HyperlinkedIdentityField(view_name='api:client_branch-detail', lookup_field='id', read_only=True)

    class Meta:
        model = Client_Branch
        fields = '__all__'