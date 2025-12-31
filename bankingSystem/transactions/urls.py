from django.urls import path
from .views import TransferView, TransactionHistoryView


urlpatterns = [

    path('transfer/', TransferView.as_view(), name='transfer'),
    path('history/', TransactionHistoryView.as_view(), name='transaction_history'),
]