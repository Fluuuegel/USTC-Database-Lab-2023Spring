import pandas as pd
from api.models import Account
from api.models import Staff
from api.models import Client
from api.models import Branch
from api.models import Client_Branch

def run():
    data = pd.read_csv("client_branch.csv", chunksize=15, header=None)

    for items in data:
        for item in items.values:
            obj = Client_Branch.objects.filter(client_id=item[0], branch_name=item[1], account_id=item[2])
            if not obj:
                client = Client.objects.get(id=item[0])
                branch = Branch.objects.get(name=item[1])
                account = Account.objects.get(id=item[2])
                o = Client_Branch.objects.create(client_id=client, branch_name=branch, account_id=account)
                o.save()


    # data = pd.read_csv("account.csv", chunksize=15, header=None)

    # for items in data:
    #     for item in items.values:
    #         obj = Account.objects.filter(id=item[0], balance=item[1], register_date=item[2], interest_rate=item[3], currency_type=item[4], staff_id=item[5])
    #         if not obj:
    #             staff = Staff.objects.get(id=item[5])
    #             o = Account.objects.create(id=item[0], balance=item[1], register_date=item[2], interest_rate=item[3], currency_type=item[4], staff_id=staff)
    #             o.save()

    # data = pd.read_csv("staff.csv", chunksize=5, header=None)

    # for items in data:
    #     insert_list = []
    #     for item in items.values:
    #         insert_list.append(Staff(id=item[0], name=item[1], phone_number=item[2], address=item[3], mail=item[4]))
    #     Staff.objects.bulk_create(insert_list)

    # data = pd.read_csv("client.csv", chunksize=15, header=None)

    # for items in data:
    #     insert_list = []
    #     for item in items.values:
    #         insert_list.append(Client(id=item[0], name=item[1], phone_number=item[2], address=item[3], mail=item[4], contact_name=item[5], contact_phone_number=item[6], contact_relationship=item[7]))
    #     Client.objects.bulk_create(insert_list)