from django.urls import path
from django.views.generic import RedirectView 
from .views import DashboardView,CreateAccountView,DepositView

urlpatterns = [
    
    path('', RedirectView.as_view(pattern_name='accounts', permanent=False)),
    
    path('accounts/', DashboardView.as_view(), name='accounts'),
    path('create/', CreateAccountView.as_view(), name='create'),
    path('deposit/<int:pk>/', DepositView.as_view(), name='deposit'),
    
]