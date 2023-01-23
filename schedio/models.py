from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class UserProfile(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    user_bio = models.TextField(max_length=500)
    profile_photo = models.URLField()
    email = models.EmailField()
    dob = models.DateField()
    user_gender = models.CharField(max_length=40)
    phone_number = PhoneNumberField()
    country = models.TextField(max_length=40)
    profession = models.TextField(max_length=50)
    organisation = models.TextField(max_length=200)

class UserPost(models.Model):
    user_id = models.IntegerField()
    image_urls = ArrayField(models.URLField(blank=True),default=list)
    post_title = models.CharField(max_length=100)
    post_gist = models.CharField(max_length=250)
    post_description = models.TextField(max_length=3000)
    likes = models.IntegerField()

