

from django.shortcuts import render, redirect
from django.views import View
from .models import User

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        national_id = request.POST.get('national_id')
        password = request.POST.get('password')

        User.objects.create(
            username=username, 
            email=email, 
            national_id=national_id, 
            password=password
        )
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.password == password:
                return redirect('dashboard')
        except User.DoesNotExist:
            pass
            
        return render(request, 'users/login.html', {'error': 'Invalid Credentials'})