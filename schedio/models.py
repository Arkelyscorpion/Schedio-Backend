from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class UserProfile(models.Model):
    username = models.CharField(max_length=60)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    user_bio = models.TextField(max_length=500,blank=True)
    tech_stack = ArrayField(models.CharField(max_length=50),default=list)
    profile_photo = models.URLField(blank=True)
    email = models.EmailField()
    dob = models.DateField()
    user_gender = models.CharField(max_length=40)
    phone_number = PhoneNumberField()
    country = models.CharField(max_length=40)
    profession = models.CharField(max_length=50)
    organisation = models.CharField(max_length=200,blank=True)
    followers = ArrayField(models.IntegerField(),default=list,blank=True)

class UserPost(models.Model):
    user_id = models.IntegerField()
    image_urls = ArrayField(models.URLField(blank=True),default=list)
    post_title = models.CharField(max_length=100)
    post_gist = models.CharField(max_length=250)
    post_description = models.TextField(max_length=3000)
    likes = models.IntegerField()

