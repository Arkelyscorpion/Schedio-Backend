from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from rest_framework import status
from .forms import CreateUserForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
# from .serializers import RegisterSerializer, UserProfileSerializer
from .serializers import *
from .models import *


def serialize_user(user):
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }


@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_data': serialize_user(user),
        'token': token
    })


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user_info": serialize_user(user),
            "token": token
        })


@api_view(['GET'])
def get_user(request):
    user = request.user
    flag = False
    if user.is_authenticated:
        flag = True
    return Response({"user_exists": flag}, status=status.HTTP_200_OK)


class registerPage(APIView):
    def post(self, request):
        username = request.data["username"]
        email = request.data["email"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        pwd1 = request.data["password1"]
        pwd2 = request.data["password2"]
        form = CreateUserForm(username=username, email=email, first_name=first_name,
                              last_name=last_name, password1=pwd1, password2=pwd2)
        registered = False
        if form.is_valid():
            form.save()
            registered = True
        return JsonResponse({'registered': registered}, safe=False)


class loginPage(APIView):
    def post(self, request):
        login_status = False
        username = request.query_params['username']
        pwd = request.query_params['password']
        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            login(request, user)
            login_status = True
        response = {'login_status': login_status}
        return JsonResponse(response, safe=False)


def logoutUser(request):
    logout(request)
    return redirect('login')


class UserProfileView(APIView):
    def get(self, reqeust):
        id = reqeust.query_params["id"]
        obj = UserProfile.objects.get(id=id)
        serializer = UserProfileSerializer(obj)
        return Response(serializer.data)

    def post(self, request):
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        user_bio = request.data["user_bio"]
        email = request.data["email"]
        dob = request.data["dob"]
        user_gender = request.data["user_gender"]
        phone_numer = request.data["phone_number"]
        country = request.data["country"]
        profession = request.data["profession"]
        organisation = request.data["organisation"]
        profle_photo_url = request.data["profile_photo"]
        user_profile_object = UserProfile(first_name=first_name,
                                          last_name=last_name,
                                          user_bio=user_bio,
                                          email=email,
                                          dob=dob,
                                          user_gender=user_gender,
                                          phone_number=phone_numer,
                                          country=country,
                                          profile_photo=profle_photo_url,
                                          profession=profession,
                                          organisation=organisation,
                                          )
        # print(user_profile_object)
        user_profile_object.save()
        return Response(status=status.HTTP_200_OK)


class UserPostView(APIView):
    def get(self, request):
        id = request.query_params["user_id"]
        obj = UserPost.objects.get(user_id=id)
        serializer = UserPostSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.data["user_id"]
        image_urls = request.data["image_urls"]
        post_title = request.data["post_title"]
        post_gist = request.data["post_gist"]
        post_desc = request.data["post_description"]
        likes = request.data["likes"]
        post_object = UserPost(user_id=user_id,
                               image_urls=image_urls,
                               post_title=post_title,
                               post_gist=post_gist,
                               post_description=post_desc,
                               likes=likes)
        post_object.save()
        return Response(status=status.HTTP_200_OK)
