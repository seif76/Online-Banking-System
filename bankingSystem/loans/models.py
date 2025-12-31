from django.db import models
from abc import ABC, abstractmethod
from decimal import Decimal
from users.models import User


class LoanCalculator(ABC):
    def __init__(self, amount, duration_months, interest_rate):
        self.amount = Decimal(amount)
        self.duration_months = duration_months
        self.interest_rate = Decimal(interest_rate)

    @abstractmethod
    def calculate_monthly_installment(self):
        pass

    @abstractmethod
    def total_payable_amount(self):
        pass


class PersonalLoanCalculator(LoanCalculator):
    def calculate_monthly_installment(self):
        total = self.total_payable_amount()
        return total / self.duration_months

    def total_payable_amount(self):
        return self.amount + (self.amount * self.interest_rate)


class HomeLoanCalculator(LoanCalculator):
    def calculate_monthly_installment(self):
        total = self.total_payable_amount()
        return total / self.duration_months

    def total_payable_amount(self):
        return self.amount + (self.amount * (self.interest_rate / 2))


class Loan(models.Model):
    LOAN_TYPES = (
        ('PERSONAL', 'Personal Loan'),
        ('HOME', 'Home Loan'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CLOSED', 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_installment = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_eligible(self, income):
        return income >= (self.amount / self.duration_months)

    def get_calculator(self):
        if self.loan_type == 'PERSONAL':
            return PersonalLoanCalculator(
                self.amount,
                self.duration_months,
                self.interest_rate
            )
        return HomeLoanCalculator(
            self.amount,
            self.duration_months,
            self.interest_rate
        )

    def approve(self):
        calculator = self.get_calculator()
        self.monthly_installment = calculator.calculate_monthly_installment()
        self.remaining_amount = calculator.total_payable_amount()
        self.status = 'APPROVED'
        self.save()

    def reject(self):
        self.status = 'REJECTED'
        self.save()

    def make_payment(self, amount):
        amount = Decimal(amount)
        if self.status != 'APPROVED':
            raise ValueError('Loan is not approved')
        if amount <= 0:
            raise ValueError('Invalid payment amount')
        if amount > self.remaining_amount:
            raise ValueError('Payment exceeds remaining amount')
 
        self.remaining_amount -= amount
        if self.remaining_amount == 0:
            self.status = 'CLOSED'
        self.save()

        return LoanPayment.objects.create(
            loan=self,
            amount=amount
        )


class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)