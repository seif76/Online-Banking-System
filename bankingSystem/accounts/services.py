from .models import SavingsAccount, CheckingAccount, BankAccount 
import uuid
from decimal import Decimal 

class GlobalATMCard:
    NUMBER = "1234-5678-9012-3456"
    CVV = "123"
    EXPIRY = "12/25"

    @staticmethod
    def validate(number, cvv, expiry):
        
        return (
            number == GlobalATMCard.NUMBER and 
            cvv == GlobalATMCard.CVV and 
            expiry == GlobalATMCard.EXPIRY
        )

class AccountCreation:

    @staticmethod
    def create_account(user, account_type, initial_balance=0):
        account_number = str(uuid.uuid4().int)[:12] 
        
        if account_type == 'SAVINGS':
            account = SavingsAccount.objects.create(
                user=user,
                account_number=account_number,
                balance=initial_balance
            )
        elif account_type == 'CHECKING':
            account = CheckingAccount.objects.create(
                user=user,
                account_number=account_number,
                balance=initial_balance
            )
        else:
            raise ValueError("Invalid account type")
            
        return account

    @staticmethod
    def apply_interest(account):
        interest = account.calculate_interest()
        if interest > 0:
            account.balance += interest
            account.save()
        return interest


    @staticmethod
    def deposit(account_id, amount, card_number, card_cvv, card_expiry):
        
        if not GlobalATMCard.validate(card_number, card_cvv, card_expiry):
            raise ValueError("Transaction Declined: Invalid Card Details")
        
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        try:
            account = BankAccount.objects.get(id=account_id)
            account.balance += Decimal(amount)
            account.save()
            return account
        except BankAccount.DoesNotExist:
            raise ValueError("Account not found")