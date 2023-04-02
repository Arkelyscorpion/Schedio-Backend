from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserPost)
admin.site.register(TechStackList)
admin.site.register(TechStackForUser)
admin.site.register(ImageUrlsForPost)
admin.site.register(TechStackForPost)
admin.site.register(UserFollowing)
