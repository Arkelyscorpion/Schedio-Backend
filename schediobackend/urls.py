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
    path('user/register/', views.register_user,name='register'),
    path('user/login/', views.login_user,name='login'),
    path('user/exist/', views.does_user_exist,name='user'),
    path('user/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('user/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('user/createprofile/',views.create_user_profile),
    path('user/myprofile/',views.get_my_details),
    path('post/myposts/',views.get_my_posts),
    path('user/getusername/',views.get_user_details),
    path('user/all/',views.get_all_users),
    path('post/all/',views.get_all_posts),
    # path('user/id/',views.UserProfileView.as_view(),name='create_user_profile'), # change dyn
    path('post/userid/',views.UserPostView.as_view()), #create dyn
    path('post/newpost/',views.create_new_post),
    path('post/id/<int:pk>',views.UserPostDetailView),
    path('user/id/<int:pk>',views.UserProfileDetailView),
    path('user/updateprofile',views.update_user_profile),
    path('post/delete/<int:id>',views.delete_post),
    path('post/userid/<int:pk>',views.user_post),
    # path('post/upload',views.AzureUpload.as_view()),
]

# send post id to get post