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
from .serializers import *
from .models import *
from django.views.generic import (CreateView,DeleteView,ListView,UpdateView,DetailView)

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user_info": serialize_user(user),
            "token": token
        })


@api_view(['POST'])
def login_user(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_data': serialize_user(user),
        'token': token
    })

@api_view(['GET'])
def does_user_exist(request):
    user = request.user
    flag = False
    if user.is_authenticated:
        flag = True
    return Response({"user_exists": flag}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user_profile(request):
    userdata = request.data.copy()
    userobj = User.objects.get(username = userdata["username"])
    tech_stack_list = request.data["tech_stack"]
    del userdata["tech_stack"]
    print(tech_stack_list)
    tech_stack_list = tech_stack_list.split(',')
    print(tech_stack_list)
    tech_stack_ids = TechStackList.objects.filter(tech_name__in=tech_stack_list)
    tids = []
    for item in tech_stack_ids:
        userdata["tech_stack"] = item.id
        tids.append(item.id)
    print(tids)
    userobj.email = request.data["email"]
    userobj.first_name = request.data["first_name"]
    userobj.last_name = request.data["last_name"]
    userobj.save()
    del userdata["email"]
    del userdata["first_name"]
    del userdata["last_name"]
    userdata["user"] = userobj.id
    # userdata["tech_stack"] = tids
    print(userdata)
    obj = UserProfile()
    obj.user = userobj
    obj.dob = request.data["dob"]
    obj.user_gender = request.data["user_gender"]
    obj.country = request.data["country"]
    obj.profession = request.data["profession"]
    obj.organisation = request.data["organisation"]
    obj.phone = request.data["phone_number"]
    obj.save()
    for items in tech_stack_ids:
        obj.tech_stack.add(items)
    obj.save()
    return Response(status=200)

@api_view(['GET'])
def get_my_details(request):
    user = request.user
    if user.is_authenticated:
        user_id = user.id
        print(user_id)
        # userObjec = UserProfile.objects.all().filter(username = username)
        userObjec = UserProfile.objects.get(user_id=user_id)
        userObjec = UserProfileSerializer(userObjec)
        return JsonResponse(userObjec.data,safe=False)

@api_view(['GET'])
def get_my_posts(request):
    user = request.user
    if user.is_authenticated:
        userid = user.id
        print(userid)
        posts=UserPostSerializer(UserPost.objects.all().filter(user=userid),many=True)
        return JsonResponse(posts.data,safe=False)
    


@api_view(['GET'])
def get_all_users(request):
    objects = User.objects.all()
    jsondata = UserSerializer(objects,many=True)
    return JsonResponse(jsondata.data,safe=False,status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_posts(request):
    posts = UserPostSerializer(UserPost.objects.all(),many=True)
    return JsonResponse(posts.data,safe=False,status=status.HTTP_200_OK)

@api_view(['POST'])
def create_new_post(request):
    print(request.data)
    obj = UserPost()
    tech_stack_list = request.data["tech_stack"]
    tech_stack_list = tech_stack_list.split(',')
    tech_stack_ids = TechStackList.objects.filter(tech_name__in=tech_stack_list)
    obj.user = User.objects.get(id=request.data["user_id"])
    obj.post_title = request.data["post_title"]
    obj.post_gist = request.data["post_gist"]
    obj.post_description = request.data["post_description"]
    obj.save()
    obj.tech_stack.set(tech_stack_ids)
    obj.save()
    colab_list = request.data["collaboraters"]
    colab_list = colab_list.split(',')
    colabs = User.objects.filter(id__in=colab_list)
    obj.collaboraters.set(colabs)
    obj.save()
    return Response(status=202)
    # serializer = UserPostSerializer(data=request.data)
    # if serializer.is_valid(raise_exception=True):
    #     serializer.save()
    #     return Response(status=status.HTTP_200_OK)
    # else:
    #     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


def serialize_user(user):
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }


@api_view(['GET'])
def UserPostDetailView(request,pk):
    queryset = UserPost.objects.all().filter(id=pk)
    obj = UserPostSerializer(queryset,many=True)
    return JsonResponse(obj.data,safe=False,status=200)

@api_view(['GET'])
def user_post(request,pk):
    queryset = UserPost.objects.filter(user_id = pk)
    obj = UserPostSerializer(queryset,many =True)
    return JsonResponse(obj.data,safe=False,status=200)

@api_view(['GET'])
def get_username(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse({"username" : user.username},safe=False)

@api_view(['GET'])
def UserProfileDetailView(request,pk):
    queryset = UserProfile.objects.get(id=pk)
    obj = UserProfileSerializer(queryset)
    return JsonResponse(obj.data,safe=False,status=200)

@api_view(['PUT'])
def update_user_profile(request):
    user = request.user
    if user.is_authenticated:
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=202)
        else:
            return Response(status=406) 
      
# still changes have to be made

@api_view(['DELETE'])
def delete_post(request,id):
    obj = UserPost.objects.get(id=id).delete()
    return Response(status=200)

@api_view(['GET'])
def like_post(request,pk):
    post = UserPost.objects.get(id = pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return Response(status=200)
    

@api_view(['GET'])
def get_user_details(request,pk):
    userobj = UserSerializer(User.objects.get(id=pk))
    return JsonResponse(userobj.data,safe=False)


@api_view(['GET'])
def get_userprofile_details(request,pk):
    profile = UserProfile.objects.get(user=pk)
    obj = UserProfileSerializer(profile)
    return JsonResponse(obj.data,safe=False)


@api_view(['GET'])
def get_post_images(request,pk):
    images = ImageUrlSerializer(ImageUrlsForPost.objects.filter(post_id=pk),many=True)
    return JsonResponse(images.data,safe=False)

@api_view(['GET'])
def get_all_userprofile(request):
    objs = UserProfileSerializer(UserProfile.objects.all(),many=True)
    return JsonResponse(objs.data,safe=False)

@api_view(['GET'])
def get_userinfo_from_token(request):
    user = request.user
    if user.is_authenticated:
        userid = user.id
        userobj = UserSerializer(User.objects.get(id=userid))
        return JsonResponse(userobj.data,safe=False)
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
        id = reqeust.query_params["user_id"]
        obj = UserProfile.objects.get(id=id)    
        serializer = UserProfileSerializer(obj)
        return Response(serializer.data)

    def post(self, request):
        username = request.data["username"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        tech_stack = request.data["tech_stack"]
        user_bio = request.data["user_bio"]
        email = request.data["email"]
        dob = request.data["dob"]
        user_gender = request.data["user_gender"]
        phone_numer = request.data["phone_number"]
        country = request.data["country"]
        profession = request.data["profession"]
        organisation = request.data["organisation"]
        profle_photo_url = request.data["profile_photo"]
        user_profile_object = UserProfile(username=username,
                                        first_name=first_name,
                                          last_name=last_name,tech_stack=tech_stack,
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
        obj = UserPost.objects.all().filter(user_id=id)
        serializer = UserPostSerializer(obj,many=True)
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
        #add time 
        return Response(status=status.HTTP_200_OK)


