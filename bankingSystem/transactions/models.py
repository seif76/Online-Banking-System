from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction
from accounts.models import BankAccount

class BaseTransaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)

    class Meta:
        abstract = True 

class Transaction(BaseTransaction):
    TRANSACTION_TYPES = [
        ('TRANSFER_OUT', 'Sent Money'),
        ('TRANSFER_IN', 'Received Money'),
    ]

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.transaction_type}: {self.amount}"

    @classmethod
    def make_transfer(cls, sender, receiver_number, amount):
        
        if sender.balance < amount:
            raise ValidationError("You don't have enough money.")

        try:
            receiver = BankAccount.objects.get(account_number=receiver_number)
        except BankAccount.DoesNotExist:
            raise ValidationError("Receiver account number is wrong.")

        with transaction.atomic():
            sender.balance -= amount
            receiver.balance += amount
            
            sender.save()
            receiver.save()

            cls.objects.create(
                account=sender, 
                amount=-amount, 
                transaction_type='TRANSFER_OUT',
                description=f"Sent to {receiver.user.username}"
            )
            cls.objects.create(
                account=receiver, 
                amount=amount, 
                transaction_type='TRANSFER_IN',
                description=f"Received from {sender.user.username}"
            )