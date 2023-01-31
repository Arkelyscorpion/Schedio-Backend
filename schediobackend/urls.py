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
    path('user/exist/', views.get_user,name='user'),
    path('user/login/', views.login,name='login'),
    path('user/register/', views.register,name='register'),
    path('user/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('user/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('user/createprofile/',views.update_profile),
    path('user/myprofile/',views.get_all_details_user),
    path('post/myposts/',views.get_my_posts),
    path('user/all/',views.get_all_users),
    path('post/all/',views.get_all_posts),
    path('user/id/',views.UserProfileView.as_view(),name='create_user_profile'), # change dyn
    path('post/userid/',views.UserPostView.as_view()), #create dyn
    path('post/newpost/',views.create_new_post),
    path('post/id/<int:pk>',views.UserPostDetailView),
    path('user/id/<int:pk>',views.UserProfileDetailView)
]

# send post id to get post