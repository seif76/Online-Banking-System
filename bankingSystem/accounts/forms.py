from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, label="Amount to Deposit ($)")
    card_number = forms.CharField(max_length=19, label="Card Number (xxxx-xxxx-xxxx-xxxx)")
    cvv = forms.CharField(max_length=3, label="CVV")
    expiry = forms.CharField(max_length=5, label="Expiry (MM/YY)")