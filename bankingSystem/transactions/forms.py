from django import forms
from accounts.models import BankAccount

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(
        queryset=BankAccount.objects.none(), 
        label="Pay From"
    )
    to_account_number = forms.CharField(label="To Account #")
    amount = forms.DecimalField(min_value=1.00, max_digits=12, decimal_places=2)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = BankAccount.objects.filter(user=user)