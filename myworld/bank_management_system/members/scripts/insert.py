import pandas as pd
from members.models import Staff

def run():
    data = pd.read_csv("staff.csv", chunksize=5)

    for items in data:
        insert_list = []
        for item in items.values:
            insert_list.append(Staff(id=item[0], name=item[1], phone_number=item[2], address=item[3], mail=item[4]))
        Staff.objects.bulk_create(insert_list)