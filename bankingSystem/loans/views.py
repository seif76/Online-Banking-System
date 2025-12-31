from decimal import Decimal
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Loan
from accounts.models import BankAccount

# class ApplyLoanView(View):
#     def get(self, request):
#         # Fetch all accounts owned by the user
#         accounts = BankAccount.objects.filter(user=request.user)
#         return render(request, 'loans/apply_loan.html', {'accounts': accounts})

#     def post(self, request):
#         account_id = request.POST.get('account_id')
#         amount = Decimal(request.POST.get('amount'))
#         term = int(request.POST.get('term'))

#         target_account = get_object_or_404(BankAccount, id=account_id, user=request.user)

#         # Instantiate the Loan object
#         loan = Loan(
#             user=request.user,
#             account=target_account,
#             amount=amount,
#             term_months=term
#         )
        
#         # This is line 30 where your error was happening
#         success, message = loan.process_instant_loan() 

#         if success:
#             return redirect('my-loans')
#         else:
#             # Re-render with an error message
#             return render(request, 'loans/apply_loan.html', {'error': message})
class ApplyLoanView(View):
    def get(self, request):
        accounts = BankAccount.objects.filter(user=request.user)
        return render(request, 'loans/apply_loan.html', {'accounts': accounts})

    def post(self, request):
        account_id = request.POST.get('account_id')
        amount_str = request.POST.get('amount', '0')
        term_str = request.POST.get('term', '6')

        try:
            amt = Decimal(amount_str)
            t = int(term_str)
            acc = get_object_or_404(BankAccount, id=account_id, user=request.user)
        except (ValueError, Decimal.InvalidOperation):
            accounts = BankAccount.objects.filter(user=request.user)
            return render(request, 'loans/apply_loan.html', {
                'accounts': accounts,
                'error_message': "Invalid amount or term selected."
            })

        loan = Loan(
            user=request.user, 
            account=acc, 
            amount=amt, 
            term_months=t
        )

        success, message = loan.process_instant_loan()

        if success:
            return redirect('/loans/my-loans/?status=approved')
        else:
            accounts = BankAccount.objects.filter(user=request.user)
            return render(request, 'loans/apply_loan.html', {
                'accounts': accounts,
                'error_message': message,  
                'prev_amount': amount_str  
            })

class MyLoansView(View):
    def get(self, request):
        loans = Loan.objects.filter(user=request.user).order_by('-created_at')
        
        status = request.GET.get('status')
        info_message = None
        
        if status == 'paid':
            info_message = "Payment processed successfully!"
        elif status == 'insufficient':
            info_message = "Error: Insufficient funds in your account."

        return render(request, 'loans/my_loans.html', {
            'loans': loans,
            'info_message': info_message
        })
class ProcessPaymentView(View):
    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id, user=request.user)
        
        success, message = loan.make_payment()
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
            
        return redirect('my-loans')       

class ProcessPaymentView(View):
    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id, user=request.user)
        
        success, message = loan.make_payment()
        
        if success:
            return redirect('/loans/my-loans/?status=paid')
        else:
            return redirect('/loans/my-loans/?status=insufficient') 