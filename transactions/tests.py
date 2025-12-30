from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Transaction, TransactionManager

class TransactionManagerTest(TestCase):
    
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        
        # Create accounts (assuming you have an Account model)
        from accounts.models import Account
        Account.objects.create(user=self.user1, balance=Decimal('1000.00'))
        Account.objects.create(user=self.user2, balance=Decimal('500.00'))
    
    def test_deposit(self):
        """Test deposit functionality"""
        transaction = TransactionManager.deposit(self.user1, Decimal('100.00'), "Test deposit")
        
        self.assertEqual(transaction.amount, Decimal('100.00'))
        self.assertEqual(transaction.balance_after, Decimal('1100.00'))
        self.assertEqual(transaction.transaction_type, 'DEPOSIT')
    
    def test_deposit_negative_amount(self):
        """Test deposit with negative amount"""
        with self.assertRaises(ValidationError):
            TransactionManager.deposit(self.user1, Decimal('-50.00'))
    
    def test_withdraw_success(self):
        """Test successful withdrawal"""
        transaction = TransactionManager.withdraw(self.user1, Decimal('200.00'), "Test withdraw")
        
        self.assertEqual(transaction.amount, Decimal('200.00'))
        self.assertEqual(transaction.balance_after, Decimal('800.00'))
        self.assertEqual(transaction.transaction_type, 'WITHDRAW')
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds (Encapsulation test)"""
        with self.assertRaises(ValidationError) as context:
            TransactionManager.withdraw(self.user1, Decimal('2000.00'))
        
        self.assertIn('Insufficient funds', str(context.exception))
    
    def test_transfer_success(self):
        """Test successful transfer"""
        transaction = TransactionManager.transfer(
            self.user1, 
            'user2', 
            Decimal('300.00'), 
            "Test transfer"
        )
        
        self.assertEqual(transaction.amount, Decimal('300.00'))
        self.assertEqual(transaction.balance_after, Decimal('700.00'))
        self.assertEqual(transaction.transaction_type, 'TRANSFER_OUT')
        
        # Check recipient received the money
        user2_balance = TransactionManager.get_balance(self.user2)
        self.assertEqual(user2_balance, Decimal('800.00'))
    
    def test_transfer_insufficient_funds(self):
        """Test transfer with insufficient funds"""
        with self.assertRaises(ValidationError):
            TransactionManager.transfer(self.user1, 'user2', Decimal('5000.00'))
    
    def test_transfer_to_self(self):
        """Test transfer to same user"""
        with self.assertRaises(ValidationError) as context:
            TransactionManager.transfer(self.user1, 'user1', Decimal('100.00'))
        
        self.assertIn('Cannot transfer to yourself', str(context.exception))
    
    def test_transfer_nonexistent_user(self):
        """Test transfer to non-existent user"""
        with self.assertRaises(ValidationError) as context:
            TransactionManager.transfer(self.user1, 'nonexistent', Decimal('100.00'))
        
        self.assertIn('Recipient not found', str(context.exception))
    
    def test_transaction_history_filter(self):
        """Test transaction history filtering"""
        TransactionManager.deposit(self.user1, Decimal('100.00'))
        TransactionManager.withdraw(self.user1, Decimal('50.00'))
        TransactionManager.deposit(self.user1, Decimal('200.00'))
        
        # Get all transactions
        all_transactions = TransactionManager.get_transaction_history(self.user1)
        self.assertEqual(all_transactions.count(), 3)
        
        # Filter by type
        deposits = TransactionManager.get_transaction_history(
            self.user1, 
            transaction_type='DEPOSIT'
        )
        self.assertEqual(deposits.count(), 2)


class TransactionModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
    
    def test_transaction_creation(self):
        """Test transaction model creation"""
        transaction = Transaction.objects.create(
            user=self.user,
            transaction_type='DEPOSIT',
            amount=Decimal('100.00'),
            balance_after=Decimal('100.00'),
            description='Test transaction'
        )
        
        self.assertEqual(str(transaction), f"DEPOSIT - 100.00 - {transaction.created_at.strftime('%Y-%m-%d %H:%M')}")
        self.assertEqual(transaction.user, self.user)
