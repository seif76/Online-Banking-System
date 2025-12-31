from django.db import models
from decimal import Decimal
from users.models import User, TimeStampedModel 

class BankAccount(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"

    def calculate_interest(self):
        return Decimal(0.00)

class SavingsAccount(BankAccount):
    interest_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.05) 

    def calculate_interest(self):
        return self.balance * self.interest_rate

class CheckingAccount(BankAccount):
    def calculate_interest(self):
        return Decimal(0.00)