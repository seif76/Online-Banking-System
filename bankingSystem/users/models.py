

from django.db import models

class User(models.Model):
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255) 
    
    is_customer = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"