from django.shortcuts import redirect
from .auth_service import AuthService
from .models import User

def jwt_required(view_func):

    def wrapper(request, *args, **kwargs):
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

        return view_func(request, *args, **kwargs)
    return wrapper