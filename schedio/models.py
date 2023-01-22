from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class UserProfile(models.Model):
    first_name= models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    user_bio = models.TextField(max_length=500)
    email = models.EmailField()
    dob = models.DateField()
    user_gender = models.CharField(max_length=40)
    phone_number =  PhoneNumberField()
    country= models.TextField(max_length=40)
    profession = models.TextField(max_length=50)
    organisation = models.TextField(max_length=200)
        
