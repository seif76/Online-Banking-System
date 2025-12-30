from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal

# Parent Transaction Model (Inheritance)
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
        ('TRANSFER_OUT', 'Transfer Out'),
        ('TRANSFER_IN', 'Transfer In'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


# Child Model - Deposits (Inheritance)
class Deposit(Transaction):
    def save(self, *args, **kwargs):
        self.transaction_type = 'DEPOSIT'
        super().save(*args, **kwargs)
    
    class Meta:
        proxy = True


# Child Model - Withdrawals (Inheritance)
class Withdrawal(Transaction):
    def save(self, *args, **kwargs):
        self.transaction_type = 'WITHDRAW'
        super().save(*args, **kwargs)
    
    class Meta:
        proxy = True


# Child Model - Transfers (Inheritance)
class Transfer(Transaction):
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_transfers')
    
    class Meta:
        proxy = False


# TransactionManager Class (Encapsulation - Critical)
class TransactionManager:
    """
    Encapsulates all transaction logic.
    Balance checks and business rules live here, NOT in views.
    """
    
    @staticmethod
    def get_balance(user):
        """Get current balance for a user"""
        from accounts.models import Account
        try:
            account = Account.objects.get(user=user)
            return account.balance
        except Account.DoesNotExist:
            return Decimal('0.00')
    
    @staticmethod
    def update_balance(user, new_balance):
        """Update user's account balance"""
        from accounts.models import Account
        account = Account.objects.get(user=user)
        account.balance = new_balance
        account.save()
    
    @classmethod
    def deposit(cls, user, amount, description=""):
        """Process a deposit transaction"""
        if amount <= 0:
            raise ValidationError("Deposit amount must be positive")
        
        current_balance = cls.get_balance(user)
        new_balance = current_balance + Decimal(str(amount))
        
        transaction = Transaction.objects.create(
            user=user,
            transaction_type='DEPOSIT',
            amount=amount,
            balance_after=new_balance,
            description=description or "Deposit"
        )
        
        cls.update_balance(user, new_balance)
        return transaction
    
    @classmethod
    def withdraw(cls, user, amount, description=""):
        """Process a withdrawal transaction"""
        if amount <= 0:
            raise ValidationError("Withdrawal amount must be positive")
        
        current_balance = cls.get_balance(user)
        
        # Critical: Balance check (Encapsulation)
        if current_balance < Decimal(str(amount)):
            raise ValidationError(f"Insufficient funds. Current balance: ${current_balance}")
        
        new_balance = current_balance - Decimal(str(amount))
        
        transaction = Transaction.objects.create(
            user=user,
            transaction_type='WITHDRAW',
            amount=amount,
            balance_after=new_balance,
            description=description or "Withdrawal"
        )
        
        cls.update_balance(user, new_balance)
        return transaction
    
    @classmethod
    def transfer(cls, sender, recipient_username, amount, description=""):
        """Process a transfer between users"""
        if amount <= 0:
            raise ValidationError("Transfer amount must be positive")
        
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            raise ValidationError("Recipient not found")
        
        if sender == recipient:
            raise ValidationError("Cannot transfer to yourself")
        
        sender_balance = cls.get_balance(sender)
        
        # Critical: Balance check (Encapsulation)
        if sender_balance < Decimal(str(amount)):
            raise ValidationError(f"Insufficient funds. Current balance: ${sender_balance}")
        
        recipient_balance = cls.get_balance(recipient)
        sender_new_balance = sender_balance - Decimal(str(amount))
        recipient_new_balance = recipient_balance + Decimal(str(amount))
        
        sender_transaction = Transfer.objects.create(
            user=sender,
            transaction_type='TRANSFER_OUT',
            amount=amount,
            balance_after=sender_new_balance,
            description=description or f"Transfer to {recipient.username}",
            recipient=recipient
        )
        
        Transfer.objects.create(
            user=recipient,
            transaction_type='TRANSFER_IN',
            amount=amount,
            balance_after=recipient_new_balance,
            description=description or f"Transfer from {sender.username}",
            recipient=sender
        )
        
        cls.update_balance(sender, sender_new_balance)
        cls.update_balance(recipient, recipient_new_balance)
        
        return sender_transaction
    
    @staticmethod
    def get_transaction_history(user, transaction_type=None, start_date=None, end_date=None):
        """Get filtered transaction history"""
        transactions = Transaction.objects.filter(user=user)
        
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)
        
        if start_date:
            transactions = transactions.filter(created_at__gte=start_date)
        
        if end_date:
            transactions = transactions.filter(created_at__lte=end_date)
        
        return transactions
