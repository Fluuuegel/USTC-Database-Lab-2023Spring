import faker

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

        relationship = ["父亲", "母亲", "子女", "其它"]

        for _ in range(num):
            id = self.fake.unique.ssn()
            name = self.fake.name()
            phone = self.fake.phone_number()
            address = self.fake.address()
            mail = self.fake.email()
            contact_name = self.fake.name()
            contact_phone_number = self.fake.phone_number()
            contact_relationship = relationship[self.fake.random_int(min=0, max=4)]
            data += f"{id},{name},{phone},{address},{mail},{contact_name},{contact_phone_number},{contact_relationship}\n"
            
        return data
        
if __name__ == "__main__":
    g = Gen()
    data = g.client(5)
    with open("../../client.csv", "w") as f:
        f.write(data)