from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Loan
from .forms import LoanApplicationForm, LoanPaymentForm


class ApplyLoanView(LoginRequiredMixin, View):
    def get(self, request):
        form = LoanApplicationForm()
        return render(request, 'loans/apply_loan.html', {'form': form})

    def post(self, request):
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.status = 'PENDING'
            loan.remaining_amount = 0
            loan.monthly_installment = 0
            loan.save()
            return redirect('my-loans')
        return render(request, 'loans/apply_loan.html', {'form': form})


class MyLoansView(LoginRequiredMixin, View):
    def get(self, request):
        loans = Loan.objects.filter(user=request.user)
        return render(request, 'loans/my_loans.html', {
            'loans': loans
        })


class PayInstallmentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk, user=request.user)
        form = LoanPaymentForm()
        return render(request, 'loans/pay_installment.html', {
            'loan': loan,
            'form': form
        })

    def post(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk, user=request.user)
        form = LoanPaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            loan.make_payment(amount)
            return redirect('my-loans')
        return render(request, 'loans/pay_installment.html', {'loan': loan, 'form': form})



class AdminLoanApprovalView(LoginRequiredMixin, View):
    def get(self, request):
        loans = Loan.objects.filter(status='PENDING')
        return render(request, 'loans/admin_approvals.html', {
            'loans': loans
        })

    def post(self, request):
        loan_id = request.POST.get('loan_id')
        action = request.POST.get('action')
        loan = get_object_or_404(Loan, pk=loan_id)
        
        if action == 'approve':
            loan.approve()
        elif action == 'reject':
            loan.reject()
            
        return redirect('admin-approvals')