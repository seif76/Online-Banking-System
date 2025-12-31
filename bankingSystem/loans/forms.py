from django import forms
from .models import Loan

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loan_type', 'amount', 'duration_months', 'interest_rate']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive")
        return amount

    def clean_duration_months(self):
        duration = self.cleaned_data.get('duration_months')
        if duration <= 0:
            raise forms.ValidationError("Duration must be at least 1 month")
        return duration


class LoanPaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Payment must be positive")
        return amount