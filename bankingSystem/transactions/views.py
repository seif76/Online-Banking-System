from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Transaction
from .forms import TransferForm

class TransferView(View):
    def get(self, request):
        form = TransferForm(user=request.user)
        return render(request, 'transactions/transfer.html', {'form': form})

    def post(self, request):
        form = TransferForm(user=request.user, data=request.POST)

        if form.is_valid():
            try:
                Transaction.make_transfer(
                    sender=form.cleaned_data['from_account'],
                    receiver_number=form.cleaned_data['to_account_number'],
                    amount=form.cleaned_data['amount']
                )
                return redirect('transaction_history')
            except ValidationError as error:
                form.add_error(None, error.message)

        return render(request, 'transactions/transfer.html', {'form': form})

class TransactionHistoryView(View):
    def get(self, request):
        transactions = Transaction.objects.filter(
            account__user=request.user
        ).order_by('-timestamp')
        
        return render(request, 'transactions/history.html', {'transactions': transactions})