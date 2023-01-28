"""schediobackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import homePage
from schedio import views
from knox import views as knox_views
urlpatterns = [
    path("admin/", admin.site.urls,name='admin'),
    path('user/', views.get_user,name='user'),
    path('login/', views.login,name='login'),
    path('register/', views.register,name='register'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('user-profile/',views.update_profile),
    path('get-username/',views.get_user_details),
    path('get-mydata/',views.get_all_details_user),
    path('get-myposts/',views.get_my_posts),
    path('get-allusers/',views.get_all_users),
    path('get-allposts/',views.get_all_posts),
    # path('user-profile/',views.UserProfileView.as_view(),name='create_user_profile'),
    path('user-post/',views.UserPostView.as_view()),
]
