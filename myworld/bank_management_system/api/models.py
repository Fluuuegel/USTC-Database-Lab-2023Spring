from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=127, primary_key=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    possession = models.DecimalField(max_digits=28, decimal_places=8)

    def __str__(self):
        return f"{self.name}"

class Staff(models.Model):
    id = models.CharField(max_length=127, primary_key=True)
    name = models.CharField(max_length=127, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    mail = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.name} {self.phone_number} {self.address} {self.mail}"

class Client(models.Model):
    id = models.CharField(max_length=127, primary_key=True)
    name = models.CharField(max_length=127, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    mail = models.CharField(max_length=255, null=True, blank=True)
    contact_name = models.CharField(max_length=127, null=True, blank=True)
    contact_phone_number = models.CharField(max_length=255, null=True, blank=True)
    contact_relationship = models.CharField(max_length=127, null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} {self.name} {self.phone_number} {self.address} {self.mail} {self.contact_name} {self.contact_phone_number} {self.contact_relationship}"
    
class Account(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    balance = models.DecimalField(max_digits=28, decimal_places=8)
    register_date = models.DateTimeField(null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=28, decimal_places=8)
    currency_type = models.CharField(max_length=255)
    staff_id = models.ForeignKey('Staff', to_field='id', null=True, blank=True, on_delete=models.RESTRICT)

class Loan(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    total = models.DecimalField(max_digits=28, decimal_places=8)
    balance = models.DecimalField(max_digits=28, decimal_places=8, default=total)
    release_date = models.DateTimeField(null=True, blank=True)
    branch_name = models.ForeignKey('Branch', to_field='name', on_delete=models.RESTRICT)
    staff_id = models.ForeignKey('Staff', to_field='id', null=True, blank=True, on_delete=models.RESTRICT)

class Client_Branch(models.Model):
    client_id = models.ForeignKey('Client', to_field='id', on_delete=models.RESTRICT)
    branch_name = models.ForeignKey('Branch', to_field='name', on_delete=models.RESTRICT)
    account_id = models.ForeignKey('Account', to_field='id', null=True, blank=True, on_delete=models.RESTRICT)

    class Meta:
        unique_together = (('client_id', 'branch_name'),)

class Client_Loan(models.Model):
    client_id = models.ForeignKey('Client', to_field='id', on_delete=models.RESTRICT)
    loan_id = models.ForeignKey('Loan', to_field='id', on_delete=models.RESTRICT)
    status = models.IntegerField(default=0) # 0: not paid, 1: paid

    class Meta:
        unique_together = (('client_id', 'loan_id'),)