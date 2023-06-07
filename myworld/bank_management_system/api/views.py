from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import IntegrityError, transaction
from django.db.models import ProtectedError

from .serializers import *

# Create your views here.

class BranchViewSet(viewsets.ModelViewSet) :
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class ClientViewSet(viewsets.ModelViewSet) :
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def update(self, request, *args, **kwargs):
        account_id = request.data.get('account_id')
        balance = request.data.get('balance')
        register_date = request.data.get('register_date')
        interest_rate = request.data.get('interest_rate')
        currency_type = request.data.get('currency_type')
        staff_id = request.data.get('staff_id')

        staff = None

        if staff_id:
            try:
                staff = Staff.objects.get(id=staff_id)
            except Staff.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Wrong staff id')

        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Wrong account id')

        
        account.balance = balance
        account.register_date = register_date
        account.interest_rate = interest_rate
        account.currency_type = currency_type

        if staff:
            account.staff_id = staff

        try:
            account.save()
            return Response(status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Update account failed')

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        account = self.get_object()

        foo = transaction.savepoint()

        try:
            client_branch = Client_Branch.objects.get(account_id=account.id)
            client_branch.account_id = None
            client_branch.save()
        except Client_Branch.DoesNotExist or IntegrityError:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Failed to delete foreign key in client_branch')

        try:
            account.delete()
        except ProtectedError:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Failed to delete account')

        transaction.savepoint_commit(foo)
        return Response(status=status.HTTP_204_NO_CONTENT)