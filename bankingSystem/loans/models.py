from django.db import models
from decimal import Decimal
from users.models import TimeStampedModel , User
from accounts.models import BankAccount


class Loan(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='loans')
    
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    term_months = models.IntegerField(default=0)
    
    interest_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    total_repayment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_installment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)
    def make_payment(self):

        if not self.is_active or self.remaining_amount <= 0:
            return False, "Loan is already fully paid."

        payment_amount = min(self.monthly_installment, self.remaining_amount)

        if self.account.balance < payment_amount:
            return False, "Insufficient funds in the linked account."

        self.account.balance -= payment_amount
        self.account.save()

        # Update Loan
        self.remaining_amount -= payment_amount
        if self.remaining_amount <= 0:
            self.remaining_amount = 0
            self.is_active = False
        self.save()

        LoanPayment.objects.create(
            loan=self,
            amount=payment_amount
        )
        return True, f"Successfully paid ${payment_amount:.2f}"
    def process_instant_loan(self):
        
        max_limit = self.account.balance * 5
        if self.amount > max_limit:
            return False, f"Rejected. Max limit for this account is ${max_limit}."

        if self.term_months <= 6:
            self.interest_rate = Decimal('0.05')
        elif self.term_months <= 12:
            self.interest_rate = Decimal('0.08')
        else:
            self.interest_rate = Decimal('0.12')

        self.total_repayment = self.amount * (1 + self.interest_rate)
        self.remaining_amount = self.total_repayment
        self.monthly_installment = self.total_repayment / self.term_months
        
        self.is_active = True
        self.account.balance += self.amount
        
        self.account.save()
        self.save()
        
        return True, "Loan approved and funds deposited!"

class LoanPayment(TimeStampedModel):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Loan {self.loan.id}"