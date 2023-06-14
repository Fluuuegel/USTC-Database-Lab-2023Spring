import pandas as pd
from api.models import *

def run():
    ## Insert loan
    # data = pd.read_csv("./data/loan.csv", chunksize=15, header=None)
    # for items in data:
    #     for item in items.values:
    #         obj = Loan.objects.filter(id=item[0], total=item[1], balance=item[2], release_date=item[3], branch_name=item[4], staff_id=item[5])
    #         if not obj:
    #             branch = Branch.objects.get(name=item[4])
    #             staff = Staff.objects.get(id=item[5])
    #             o = Loan.objects.create(id=item[0], total=item[1], balance=item[2], release_date=item[3], branch_name=branch, staff_id=staff)
    #             o.save()

    ## Insert client_loan
    data = pd.read_csv("./data/client_loan.csv", chunksize=15, header=None)
    for items in data:
        for item in items.values:
            obj = Client_Loan.objects.filter(client_id=item[0], loan_id=item[1], status=item[2])
            if not obj:
                client = Client.objects.get(id=item[0])
                loan = Loan.objects.get(id=item[1])
                o = Client_Loan.objects.create(client_id=client, loan_id=loan, status=item[2])
                o.save()
    
    ## Insert client_branch
    # data = pd.read_csv("./data/client_branch.csv", chunksize=15, header=None)
    # for items in data:
    #     for item in items.values:
    #         obj = Client_Branch.objects.filter(client_id=item[0], branch_name=item[1], account_id=item[2])
    #         if not obj:
    #             client = Client.objects.get(id=item[0])
    #             branch = Branch.objects.get(name=item[1])
    #             account = Account.objects.get(id=item[2])
    #             o = Client_Branch.objects.create(client_id=client, branch_name=branch, account_id=account)
    #             o.save()

    ## Insert account
    # data = pd.read_csv("account.csv", chunksize=15, header=None)
    # for items in data:
    #     for item in items.values:
    #         obj = Account.objects.filter(id=item[0], balance=item[1], register_date=item[2], interest_rate=item[3], currency_type=item[4], staff_id=item[5])
    #         if not obj:
    #             staff = Staff.objects.get(id=item[5])
    #             o = Account.objects.create(id=item[0], balance=item[1], register_date=item[2], interest_rate=item[3], currency_type=item[4], staff_id=staff)
    #             o.save()

    ## Insert staff
    # data = pd.read_csv("staff.csv", chunksize=5, header=None)
    # for items in data:
    #     insert_list = []
    #     for item in items.values:
    #         insert_list.append(Staff(id=item[0], name=item[1], phone_number=item[2], address=item[3], mail=item[4]))
    #     Staff.objects.bulk_create(insert_list)

    ## Insert client
    # data = pd.read_csv("client.csv", chunksize=15, header=None)
    # for items in data:
    #     insert_list = []
    #     for item in items.values:
    #         insert_list.append(Client(id=item[0], name=item[1], phone_number=item[2], address=item[3], mail=item[4], contact_name=item[5], contact_phone_number=item[6], contact_relationship=item[7]))
    #     Client.objects.bulk_create(insert_list)

    ## Insert branch
    # data = pd.read_csv("branch.csv", chunksize=3, header=None)
    # for items in data:
    #     insert_list = []
    #     for item in items.values:
    #         insert_list.append(Branch(name=item[0], city=item[1], possession=item[2]))
    #     Branch.objects.bulk_create(insert_list)