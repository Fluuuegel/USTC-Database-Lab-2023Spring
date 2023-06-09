import faker
import random

class Gen:
    def __init__(self):
        self.fake = faker.Faker(locale='ja_JP')

    def staff(self, num):
        data = ""
        for _ in range(num):
            id = self.fake.unique.ssn()
            name = self.fake.name()
            phone = self.fake.phone_number()
            address = self.fake.address()
            mail = self.fake.email()
            data += f"{id},{name},{phone},{address},{mail}\n"
        return data
    
    def client(self, num):
        data = ""

        relationship = ["お父さん", "お母さん", "子", "セックス", "その他"]

        for _ in range(num):
            id = self.fake.unique.ssn()
            name = self.fake.name()
            phone = self.fake.phone_number()
            address = self.fake.address()
            mail = self.fake.email()
            contact_name = self.fake.name()
            contact_phone_number = self.fake.phone_number()
            contact_relationship = relationship[random.randint(0, 4)]
            data += f"{id},{name},{phone},{address},{mail},{contact_name},{contact_phone_number},{contact_relationship}\n"
            
        return data
    
    def account(self, num):
        data = ""

        staffs = ["173-25-1480", "067-84-8258", "141-66-1428", "652-98-0341", "718-98-9270"]

        for _ in range(num):
            id = str(self.fake.unique.random_int(min=100, max=999))
            balance = float(random.randint(0, 1000000))
            register_date = self.fake.date_time_between(start_date='-1y', end_date='now', tzinfo=None)
            interest_rate = 1.02
            currency_type = "JPY"
            staff_id = staffs[random.randint(0, 4)]
            data += f"{id},{balance},{register_date},{interest_rate},{currency_type},{staff_id}\n"
        
        return data
        
if __name__ == "__main__":
    g = Gen()

    data = g.account(15)
    with open("../../data/account.csv", "w") as f:
        f.write(data)


    # data = g.staff(5)
    # with open("../../staff.csv", "w") as f:
    #     f.write(data)

    # data = g.client(15)
    # with open("../../client.csv", "w") as f:
    #     f.write(data)