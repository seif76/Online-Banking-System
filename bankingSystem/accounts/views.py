from django.shortcuts import render, redirect ,get_object_or_404
from django.views import View
from .models import BankAccount
from .services import AccountCreation
from .forms import DepositForm 
class DashboardView(View):
    def get(self, request):
        user_accounts = BankAccount.objects.filter(user=request.user)
        context = {
            'accounts': user_accounts,
            'user': request.user
        }
        return render(request, 'accounts/dashboard.html', context)

class CreateAccountView(View):
    def get(self, request):
        return render(request, 'accounts/create_account.html')

    def post(self, request):
        account_type = request.POST.get('account_type')
        
        try:
            AccountCreation.create_account(
                user=request.user,
                account_type=account_type
            )
            return redirect('accounts')
            
        except ValueError as e:
            return render(request, 'accounts/create_account.html', {'error': str(e)})
        
class DepositView(View):
    def get(self, request, pk):
        account = get_object_or_404(BankAccount, pk=pk, user=request.user)
        form = DepositForm()
        return render(request, 'accounts/deposit.html', {'form': form, 'account': account})

    def post(self, request, pk):
        account = get_object_or_404(BankAccount, pk=pk, user=request.user)
        form = DepositForm(request.POST)

        if form.is_valid():
            try:
                AccountCreation.deposit(
                    account_id=account.id,
                    amount=form.cleaned_data['amount'],
                    card_number=form.cleaned_data['card_number'],
                    card_cvv=form.cleaned_data['cvv'],
                    card_expiry=form.cleaned_data['expiry']
                )
                return redirect('accounts') 
            
            except ValueError as e:
                return render(request, 'accounts/deposit.html', {
                    'form': form, 
                    'account': account, 
                    'error': str(e)
                })
        
        return render(request, 'accounts/deposit.html', {'form': form, 'account': account})