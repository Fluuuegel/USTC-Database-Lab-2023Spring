import pandas as pd
from api.models import Client

def run():
    data = pd.read_csv("client.csv", chunksize=5, header=None)

    for items in data:
        insert_list = []
        for item in items.values:
            insert_list.append(Client(id=item[0], name=item[1], phone_number=item[2], address=item[3], mail=item[4], contact_name=item[5], contact_phone_number=item[6], contact_relationship=item[7]))
        Client.objects.bulk_create(insert_list)