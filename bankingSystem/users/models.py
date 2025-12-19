from django.db import models


class TimeStampedModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # this means that this will note be a db table



class User(TimeStampedModel): 
  
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    
    
    password = models.CharField(max_length=255) 
    
    is_customer = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)

    
    def __str__(self):
        return self.username

    
    def get_role(self):
        if self.is_employee:
            return "Bank Employee"
        return "Valued Customer"


class Profile(TimeStampedModel): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    
    @property
    def full_contact(self):
        addr = self.address if self.address else "No Address"
        phone = self.phone_number if self.phone_number else "No Phone"
        return f"{addr} | {phone}"