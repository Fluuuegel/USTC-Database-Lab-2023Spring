import faker

class Gen:
    def __init__(self):
        self.fake = faker.Faker(locale='zh_CN')

    def staff(self, num):
        data = ""
        for i in range(num):
            id = self.fake.unique.ssn()
            name = self.fake.name()
            phone = self.fake.phone_number()
            address = self.fake.address()
            mail = self.fake.email()
            data += f"{id},{name},{phone},{address},{mail}\n"
        return data
        
if __name__ == "__main__":
    g = Gen()
    data = g.staff(5)
    with open("../../staff.csv", "w") as f:
        f.write(data)