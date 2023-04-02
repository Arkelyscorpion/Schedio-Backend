from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class TechStackList(models.Model):
    tech_name = models.CharField(
        max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.tech_name
    
# class UserProfile(models.Model):
#     username = models.CharField(max_length=60,unique=True)
#     first_name = models.CharField(max_length=40)
#     last_name = models.CharField(max_length=40)
#     user_bio = models.TextField(max_length=500,blank=True)
#     tech_stack = ArrayField(models.CharField(max_length=50),default=list)
#     profile_photo = models.URLField(blank=True)
#     email = models.EmailField(unique=True)
#     dob = models.DateField()
#     user_gender = models.CharField(max_length=40)
#     phone_number = PhoneNumberField()
#     country = models.CharField(max_length=40)
#     profession = models.CharField(max_length=50)
#     organisation = models.CharField(max_length=200,blank=True)
#     followers = ArrayField(models.IntegerField(),default=list,blank=True)

#     def __str__(self):
#         return self.username
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    user_bio = models.TextField(max_length=500,blank=True)
    profile_photo = models.URLField(blank=True)
    dob = models.DateField(blank=True)
    user_gender = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    profession = models.CharField(max_length=50)
    organisation = models.CharField(max_length=200,blank=True)
    tech_stack = models.ManyToManyField(TechStackList,blank=True)

    def __str__(self):
        return self.user_bio
    

class TechStackForUser(models.Model):
    user_id = models.ForeignKey(UserProfile,on_delete =models.CASCADE)
    tech_name_id = models.ForeignKey(TechStackList,on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.user_id} knows {self.tech_name_id}')
    
    class Meta:
        unique_together = ('user_id','tech_name_id')

# class UserPost(models.Model):
#     user_id = models.IntegerField()
#     image_urls = ArrayField(models.URLField(blank=True),default=list(["https://picsum.photos/seed/picsum/800/600"]))
#     post_title = models.CharField(max_length=100)
#     post_gist = models.CharField(max_length=250)
#     post_description = models.TextField(max_length=3000)
#     time_created = models.DateTimeField(auto_now=False,auto_now_add=True)
#     last_edit = models.DateTimeField(auto_now=True)
#     likes = models.ManyToManyField(User,related_name='post_like')
#     tech_stack = ArrayField(models.CharField(max_length=50),default=list)
    
#     def number_of_likes(self):
#         return self.likes.count()
    
#     def __str__(self): 
#         return self.post_title

class UserPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.FileField(blank=False,null=False)
    post_title = models.CharField(max_length=100)
    post_gist = models.CharField(max_length=250)
    post_description = models.TextField(max_length=3000)
    time_created = models.DateTimeField(auto_now=False,auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,related_name='post_like')
    tech_stack = models.ManyToManyField(TechStackList,related_name='tech_stack',blank=True)
    collaboraters = models.ManyToManyField(User,related_name='collaboraters')
    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.post_title

class ImageUrlsForPost(models.Model):
    post_id = models.ForeignKey(UserPost,on_delete=models.CASCADE)
    image_url = models.URLField(blank=False)
    
    class Meta:
        unique_together = ('post_id','image_url')

class TechStackForPost(models.Model):
    post_id = models.ForeignKey(UserPost,on_delete=models.CASCADE)
    tech_name = models.ForeignKey(TechStackList,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post_id','tech_name')


class UserFollowing(models.Model):
    user = models.ForeignKey(User,related_name="follwing",on_delete=models.CASCADE)
    following_user = models.ForeignKey(User,related_name="followers",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'{self.user.username} following {self.following_user.username}')
    class Meta:
        unique_together = ('user','following_user')