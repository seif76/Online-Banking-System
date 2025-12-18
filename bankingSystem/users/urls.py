from django.urls import path
from django.views.generic import RedirectView # Import this
from .views import RegisterView, LoginView

urlpatterns = [
    
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]