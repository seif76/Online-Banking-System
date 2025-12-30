from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('withdraw/', views.WithdrawView.as_view(), name='withdraw'),
    path('transfer/', views.TransferView.as_view(), name='transfer'),
    path('history/', views.TransactionHistoryView.as_view(), name='transaction_history'),
    path('print-statement/', views.print_statement, name='print_statement'),
]