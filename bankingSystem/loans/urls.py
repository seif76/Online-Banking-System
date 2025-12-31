

from django.urls import path
from .views import ApplyLoanView, MyLoansView, ProcessPaymentView
from django.views.generic import RedirectView 
urlpatterns = [   
   path('', RedirectView.as_view(pattern_name='my-loans', permanent=False)),
    path('apply/', ApplyLoanView.as_view(), name='apply-loan'),
    path('my-loans/', MyLoansView.as_view(), name='my-loans'),
    path('pay/<int:loan_id>/', ProcessPaymentView.as_view(), name='process-payment'),
]