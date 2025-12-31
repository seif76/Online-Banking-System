from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from .auth_service import AuthService
from .models import User

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_url_names = [
            'login',
            'register',
        ]

    def __call__(self, request):
        
        public_paths = []
        for name in self.public_url_names:
            try:
                public_paths.append(reverse(name))
            except NoReverseMatch:
                continue 

        
        if request.path in public_paths:
            return self.get_response(request)

       
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)


        token = request.COOKIES.get('access_token')

        
        if not token:
            return redirect('login')

        user_id = AuthService.decode_jwt(token)
        if not user_id:
            return redirect('login')

        try:
            request.user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('login')

        return self.get_response(request)