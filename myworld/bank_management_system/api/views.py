from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import random

from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.utils import timezone

from .serializers import *

# Create your views here.

class BranchViewSet(viewsets.ModelViewSet) :
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'name'

    @action(detail=False, methods=['post'])
    def statisticize(self, request):

        radio = request.data.get('radio')

        branches = Branch.objects.all()
        accounts = Account.objects.all()
        loan = Loan.objects.all()
        data = []

        if radio == 'Seasonly':
            month_lower_bound = ((timezone.now().month - 1) // 3) * 3 + 1
            month_upper_bound = ((timezone.now().month - 1) // 3) * 3 + 3
            accounts = accounts.filter(register_date__month__gte=month_lower_bound, register_date__month__lte=month_upper_bound)
            loan = loan.filter(release_date__month__gte=month_lower_bound, release_date__month__lte=month_upper_bound)
        elif radio == 'Monthly':
            accounts = accounts.filter(register_date__month=timezone.now().month)
            loan = loan.filter(release_date__month=timezone.now().month)

        elif radio == 'Last Year':
            accounts = accounts.filter(register_date__year__gte=timezone.now().year - 2, register_date__year__lte=timezone.now().year - 1)
            loan = loan.filter(release_date__year__gte=timezone.now().year - 2, release_date__year__lte=timezone.now().year - 1)

        for branch in branches:
            data.append({
                'branch_name': branch.name,
                'account_num': 0,
                'saving': 0,
                'loan': 0
            })
            for client_branch in Client_Branch.objects.filter(branch_name=branch.name):
                try:
                    account = accounts.get(id=client_branch.account_id_id)
                    data[-1]['account_num'] += 1
                    data[-1]['saving'] += account.balance
                except Account.DoesNotExist:
                    pass
            for loan in Loan.objects.filter(branch_name=branch.name):
                data[-1]['loan'] += loan.total

        return Response(status=status.HTTP_200_OK, data=data)

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = 'id'

class ClientSearchViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'id'

    def get_queryset(self):
        text_fields = ['id', 'name', 'phone_number', 'address', 'contact_name', 'contact_phone_number',
                       'contact_email', 'contact_relationship']
        queryset = self.queryset
        for text_field in text_fields:
            query_param = self.request.query_params.get(text_field)
            if query_param:
                queryset = queryset.filter(**{f'{text_field}__icontains': query_param})
        return queryset

class ClientViewSet(viewsets.ModelViewSet) :
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'id'

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        client = self.get_object()

        foo = transaction.savepoint()

        try: 
            client.delete()
        except :
            try:
                client_branch = Client_Branch.objects.get(client_id=client.id)
            except Client_Branch.DoesNotExist:
                transaction.savepoint_rollback(foo)
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Client_Branch does not exist')
            
            client_branch.delete()
            client.delete()
            transaction.savepoint_commit(foo)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        transaction.savepoint_commit(foo)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = 'id'

    # update 
    def update(self, request, *args, **kwargs):
        loan_id = request.data.get('loan_id')
        balance = request.data.get('balance')

        try:
            loan = Loan.objects.get(id=loan_id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Wrong loan id')

        loan.balance = balance

        # trigger
        if(balance == 0):
            status = 1

        try:
            loan.save()
            return Response(status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Update loan failed')

    # delete loan
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        loan = self.get_object()

        foo = transaction.savepoint()

        try:
            client_loan = Client_Loan.objects.get(loan_id=loan.id)
            client_loan.loan_id = None
            client_loan.save()
        except Client_Branch.DoesNotExist or IntegrityError:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Failed to delete foreign key in client_loan')

        try:
            loan.delete()
        except ProtectedError:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Failed to delete loan')

        transaction.savepoint_commit(foo)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ClientLoanViewSet(viewsets.ModelViewSet):
    queryset = Client_Loan.objects.all()
    serializer_class = Client_LoanSerializer
    lookup_field = 'id'

    def get_queryset(self):
        related_fields = ['client_id', 'loan_id']
        queryset = self.queryset
        for related_field in related_fields:
            query_param = self.request.query_params.get(related_field)
            if query_param:
                queryset = queryset.filter(
                    **{f'{related_field}__{related_field.split("_")[-1]}__icontains': query_param}
                )
        return queryset
    
    # release loan
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def release_loan(self, request):
        client_id = request.data.get('client_id')
        total = request.data.get('total')
        branch_name = request.data.get('branch_name')
        staff_id = request.data.get('staff_id')

        if not (client_id and total and branch_name):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Parameter incomplete')

        if not (total <= 0):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Total must be positive')
        
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
            client_loan = Client_Loan.objects.create(client_id=client)
        except IntegrityError:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Failed to create client_loan')

        loan = None
        for _ in range(10):
            loan_id = str(random.randint(100, 9999))
            try:
                loan = Loan.objects.create(
                    id=loan_id,
                    total=total,
                    balance=total,
                    release_date=timezone.now(),
                    branch_name=branch,
                    staff_id=staff,
                )
                break
            except IntegrityError:
                continue
        if not loan:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Failed to create loan')

        try:
            client_loan.loan_id = loan
            client_loan.status = 0
            client_loan.save()
            transaction.savepoint_commit(foo)
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            transaction.savepoint_rollback(foo)
            return Response(status=status.HTTP_201_CREATED)

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