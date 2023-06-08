from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import random

from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.utils import timezone
from decimal import Decimal

from .serializers import *

# Create your views here.

class BranchViewSet(viewsets.ModelViewSet) :
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'id'

class ClientViewSet(viewsets.ModelViewSet) :
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'id'

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = 'id'

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'

    # update 
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

    # delete account
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
    
class ClientBranchViewSet(viewsets.ModelViewSet):
    queryset = Client_Branch.objects.all()
    serializer_class = Client_BranchSerializer
    lookup_field = 'id'

    def get_queryset(self):
        related_fields = ['client_id', 'branch_name', 'account_id']
        queryset = self.queryset
        for related_field in related_fields:
            query_param = self.request.query_params.get(related_field)
            if query_param:
                queryset = queryset.filter(
                    **{f'{related_field}__{related_field.split("_")[-1]}__icontains': query_param}
                )
        return queryset

    # open account
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def open_account(self, request):
        client_id = request.data.get('client_id')
        branch_name = request.data.get('branch_name')
        currency_type = request.data.get('currency_type')
        interest_rate = request.data.get('interest_rate')
        staff_id = request.data.get('staff_id')

        if not (client_id and branch_name and currency_type and interest_rate):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Parameter incomplete')

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Client does not exist')

        try:
            branch = Branch.objects.get(name=branch_name)
        except Branch.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Branch does not exist')

        staff = None
        if staff_id:
            try:
                staff = Staff.objects.get(id=staff_id)
            except Staff.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Staff does not exist')

        foo = transaction.savepoint()

        try:
            client_branch = Client_Branch.objects.get(client_id=client_id, branch_name=branch_name)
            if client_branch.account_id:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Client already has a account')
        except Client_Branch.DoesNotExist:
            try:
                client_branch = Client_Branch.objects.create(client_id=client, branch_name=branch)
            except IntegrityError:
                transaction.savepoint_rollback(foo)
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Failed to create client_branch')

        account = None
        for _ in range(10):
            account_id = str(random.randint(100, 9999))
            try:
                account = Account.objects.create(
                    id=account_id,
                    balance=0,
                    register_date=timezone.now(),
                    interest_rate=interest_rate,
                    currency_type=currency_type,
                    staff_id=staff,
                )
                break
            except IntegrityError:
                continue
        if not account:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Failed to create account')

        try:
            client_branch.account_id = account
            client_branch.save()
            transaction.savepoint_commit(foo)
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_201_CREATED)