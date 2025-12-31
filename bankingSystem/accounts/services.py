import uuid
from .models import SavingsAccount, CheckingAccount

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