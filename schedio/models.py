from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class UserProfile(models.Model):
    username = models.CharField(max_length=60,unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    user_bio = models.TextField(max_length=500,blank=True)
    tech_stack = ArrayField(models.CharField(max_length=50),default=list)
    profile_photo = models.URLField(blank=True)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    user_gender = models.CharField(max_length=40)
    phone_number = PhoneNumberField()
    country = models.CharField(max_length=40)
    profession = models.CharField(max_length=50)
    organisation = models.CharField(max_length=200,blank=True)
    followers = ArrayField(models.IntegerField(),default=list,blank=True)

    def __str__(self):
        return self.username

class UserPost(models.Model):
    user_id = models.IntegerField()
    image_urls = ArrayField(models.URLField(blank=True),default=list(["https://picsum.photos/seed/picsum/800/600"]))
    post_title = models.CharField(max_length=100)
    post_gist = models.CharField(max_length=250)
    post_description = models.TextField(max_length=3000)
    time_created = models.DateTimeField(auto_now=False,auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(blank=True,null=True,default=0)
    tech_stack = ArrayField(models.CharField(max_length=50),default=list)
    
    def __str__(self): 
        return self.post_title

