import pandas as pd
from api.models import Branch

def run():
    data = pd.read_csv("branch.csv", chunksize=3, header=None)

    for items in data:
        insert_list = []
        for item in items.values:
            insert_list.append(Branch(name=item[0], city=item[1], possession=item[2]))
        Branch.objects.bulk_create(insert_list)