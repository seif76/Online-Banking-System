from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from .models import Transaction, TransactionManager
from .forms import DepositForm, WithdrawForm, TransferForm, TransactionFilterForm
from datetime import datetime

# Class-Based Views for Payments

class DepositView(LoginRequiredMixin, FormView):
    """Handle deposit transactions"""
    template_name = 'transactions/deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('transaction_history')
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        description = form.cleaned_data.get('description', '')
        
        try:
            transaction = TransactionManager.deposit(
                user=self.request.user,
                amount=amount,
                description=description
            )
            messages.success(
                self.request,
                f'Successfully deposited ${amount}. New balance: ${transaction.balance_after}'
            )
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_balance'] = TransactionManager.get_balance(self.request.user)
        return context


class WithdrawView(LoginRequiredMixin, FormView):
    """Handle withdrawal transactions"""
    template_name = 'transactions/withdraw.html'
    form_class = WithdrawForm
    success_url = reverse_lazy('transaction_history')
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        description = form.cleaned_data.get('description', '')
        
        try:
            transaction = TransactionManager.withdraw(
                user=self.request.user,
                amount=amount,
                description=description
            )
            messages.success(
                self.request,
                f'Successfully withdrew ${amount}. New balance: ${transaction.balance_after}'
            )
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_balance'] = TransactionManager.get_balance(self.request.user)
        return context


class TransferView(LoginRequiredMixin, FormView):
    """Handle transfer transactions"""
    template_name = 'transactions/transfer.html'
    form_class = TransferForm
    success_url = reverse_lazy('transaction_history')
    
    def form_valid(self, form):
        recipient_username = form.cleaned_data['recipient_username']
        amount = form.cleaned_data['amount']
        description = form.cleaned_data.get('description', '')
        
        try:
            transaction = TransactionManager.transfer(
                sender=self.request.user,
                recipient_username=recipient_username,
                amount=amount,
                description=description
            )
            messages.success(
                self.request,
                f'Successfully transferred ${amount} to {recipient_username}. New balance: ${transaction.balance_after}'
            )
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_balance'] = TransactionManager.get_balance(self.request.user)
        return context


class TransactionHistoryView(LoginRequiredMixin, ListView):
    """Display transaction history with filters"""
    model = Transaction
    template_name = 'transactions/transaction_history.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Apply filters
        transaction_type = self.request.GET.get('transaction_type')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TransactionFilterForm(self.request.GET)
        context['current_balance'] = TransactionManager.get_balance(self.request.user)
        return context


def print_statement(request):
    """Generate printable statement"""
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    transaction_type = request.GET.get('transaction_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    transactions = TransactionManager.get_transaction_history(
        user=request.user,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date
    )
    
    context = {
        'transactions': transactions,
        'user': request.user,
        'current_balance': TransactionManager.get_balance(request.user),
        'generated_at': datetime.now(),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'transactions/print_statement.html', context)

