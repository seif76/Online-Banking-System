from django.shortcuts import render, redirect
from django.views import View
from .models import User
from .auth_service import AuthService 

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        national_id = request.POST.get('national_id')
        password = request.POST.get('password')

        address = request.POST.get('address')
        phone = request.POST.get('phone_number')

        hashed_password = AuthService.hash_password(password)

        user = User.objects.create(
            username=username, 
            email=email, 
            national_id=national_id, 
            password=hashed_password
        )

        user.profile.address = address
        user.profile.phone_number = phone
        user.profile.save() 
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            
            if AuthService.verify_password(password, user.password):
                
                token = AuthService.generate_jwt(user.id)

                
                response = redirect('profile')
                response.set_cookie('access_token', token, httponly=True)
                
                
                return response
                
        except User.DoesNotExist:
            pass
            
        return render(request, 'users/login.html', {'error': 'Invalid Credentials'})
    

class LogoutView(View):
    def get(self, request):
        response = redirect('login')
        response.delete_cookie('access_token')
        return response
    
# @method_decorator(jwt_required, name='dispatch')    
class ProfileView(View):
    def get(self, request):

        return render(request, 'users/profile.html', {
            'user': request.user
        })