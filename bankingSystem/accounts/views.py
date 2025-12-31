from django.shortcuts import render, redirect
from django.views import View
# REMOVED: from django.contrib import messages 
from .models import BankAccount
from .services import AccountCreation

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
            # Success: Just redirect, no message
            return redirect('accounts')
            
        except ValueError as e:
            # Error: Pass the error string manually to the template
            return render(request, 'accounts/create_account.html', {'error': str(e)})