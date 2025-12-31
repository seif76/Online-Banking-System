from django.urls import path
from django.views.generic import RedirectView 
from .views import ApplyLoanView, MyLoansView, PayInstallmentView, AdminLoanApprovalView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='my-loans', permanent=False)),
    path('apply/', ApplyLoanView.as_view(), name='apply-loan'),
    path('my-loans/', MyLoansView.as_view(), name='my-loans'),
    path('pay/<int:pk>/', PayInstallmentView.as_view(), name='pay-installment'),
    path('admin/approvals/', AdminLoanApprovalView.as_view(), name='admin-approvals'),
]