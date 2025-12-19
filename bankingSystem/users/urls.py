from django.urls import path
from django.views.generic import RedirectView 
from .views import RegisterView, LoginView , ProfileView,LogoutView

urlpatterns = [
    
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]