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
from azure.storage.blob import ContainerClient
import os
from django.utils.safestring import mark_safe
from knox.auth import AuthToken
from rest_framework import status
from .forms import CreateUserForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import *
from .models import *
import yaml
import json
from django.conf import settings
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


@api_view(['PUT'])
def edit_user_profile(request):
    # userdata = request.data.copy()
    userprofileobj = UserProfile.objects.get(username=request.data["username"])
    userprofileobj.user_bio = request.data["user_bio"]
    userprofileobj.dob = request.data["dob"]
    userprofileobj.user_gender = request.data["user_gender"]
    userprofileobj.country = request.data["country"]
    userprofileobj.profession = request.data["profession"]
    userprofileobj.organisation = request.data["organisation"]
    userprofileobj.phone = request.data["phone_number"]
    userprofileobj.linkedin = request.data["linkedin"]
    userprofileobj.github = request.data["github"]
    userprofileobj.save()
    tech_stack_list = request.data["tech_stack"]
    tech_stack_list = tech_stack_list.split(',')
    tech_stack_ids = TechStackList.objects.filter(
        tech_name__in=tech_stack_list)
    for items in tech_stack_ids:
        userprofileobj.tech_stack.add(items)
    userprofileobj.save()
    try:
        userprofileobj.file = request.data["file"]
        userprofileobj.save()
        fileobj = request.data["file"]
        config = load_config()
        x = str(userprofileobj.file).split('/')
        link = upload(fileobj.name, settings.MEDIA_ROOT+'\\' +
                      x[0] + '\\' + x[1], config["azure_storage_connectionstring"], config["container_name"])
        userprofileobj.image_url = link
        userprofileobj.save()
    except:
        return JsonResponse({"status" : "failed to add profile photo"},status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_202_ACCEPTED)



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
    try:
        obj.file = request.data["file"]
        obj.save()
        fileobj = request.data["file"]
        config = load_config()
        x = str(obj.file).split('/')
        link = upload(fileobj.name, settings.MEDIA_ROOT+'\\' +
                    x[0] + '\\' + x[1], config["azure_storage_connectionstring"], config["container_name"])
        obj.image_url = link
        obj.save()
    except:
        return Response(status=200)
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


def post_serializer_json(post):
    return {
        "id" : post.id,
        "user_id" : str(post.user),
        "file" : str(post.file),
        "post_title" : post.post_title,
        "post_gist" : post.post_gist,
        "post_description" : post.post_description,
        "time_created" : post.time_created,
        "last_edit" : post.last_edit,
        "likes" : str(post.likes),
        "tech_stack" : str(post.tech_stack),
        "collaboraters" : str(post.collaboraters),
        "status" : post.status,
    }

# def get_stack_name(ids):


@api_view(['POST'])
def get_stack_names(request):
    l = request.data["tech_stack"]
    objs = TechStackSerializer(TechStackList.objects.filter(id__in=l),many=True)
    return JsonResponse(objs.data,safe=False)
    return Response(status=200)

@api_view(['GET'])
def get_all_posts(request):
    posts = UserPost.objects.all()
    qs = posts.order_by('-time_created')
    posts = UserPostSerializer(qs,many=True)

    # ?x = json.loads(UserPost.objects.all())
    # print(x)
    # l = []
    # for items in posts:
    #     l.append(post_serializer_json(items))
    # print(l)
    # # y = list(UserPost.objects.all().values())
    # # print(y)
    # # x = JsonResponse({"data":y})
    # # print(x)
    # # x = []
    # # for items in y:
    # #     print(post_serializer_json(items))
    # # print(x)
    # return JsonResponse({"data" : l},safe=False)
    # return Response(status=200)
    # posts = UserPost.objects.get(id=9)
    # techs = TechStackList.objects.get(id=1)
    # data = {
    #     'posts' : posts.collaboraters,
    #     'techs' : techs
    # }
    # data = mark_safe(json.dumps(data))
    return JsonResponse(posts.data,safe=False,status=status.HTTP_200_OK)


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + '/config.yaml', 'r') as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)


def upload(file, path, connection_string, container_name):
    container_client = ContainerClient.from_connection_string(
        connection_string, container_name)
    print("uploading")
    blob_client = container_client.get_blob_client(file)
    with open(path, "rb") as data:
        blob_client.upload_blob(data)
        print("done")
        return blob_client.url

@api_view(['PUT'])
def edit_user_post(request):

    postobj = UserPost.objects.get(id=request.data["id"])
    # UserPost.objects.get(id=request.data["id"]).update(data=request.data)
    
    print(postobj.id)
    print(postobj.post_title)
    postobj.post_title = request.data["post_title"]
    postobj.post_gist = request.data["post_gist"]
    postobj.post_description = request.data["post_description"]
    postobj.status = request.data["status"]
    postobj.save()
    tech_stack_list = request.data["tech_stack"]
    tech_stack_list = tech_stack_list.split(',')
    tech_stack_ids = TechStackList.objects.filter(
        tech_name__in=tech_stack_list)
    postobj.tech_stack.set(tech_stack_ids)
    postobj.save()
    colab_list = request.data["collaboraters"]
    colab_list = colab_list.split(',')
    colabs = User.objects.filter(id__in=colab_list)
    postobj.collaboraters.set(colabs)
    postobj.save()
    try:
        fileobj = request.data["file"]
        print(fileobj.name)
        config = load_config()
        x = str(postobj.file).split('/')
        link = upload(fileobj.name, settings.MEDIA_ROOT+'\\' +
                      x[0] + '\\' + x[1], config["azure_storage_connectionstring"], config["container_name"])
        print(settings.MEDIA_ROOT+'\\' + x[0] + '\\' + x[1])
        print(postobj.file)
        print(link)
        postobj.image_url = link
        postobj.save()
    except:
        return JsonResponse({"status" : "failed to upload photo"},status=status.HTTP_200_OK)
    # postobj.data = request.data
    # postobj.save()
    return Response(status=202)

@api_view(['POST'])
def create_new_post(request):
    print(request.data)
    obj = UserPost()
    tech_stack_list = request.data["tech_stack"]
    tech_stack_list = tech_stack_list.split(',')
    print(tech_stack_list)
    tech_stack_ids = TechStackList.objects.filter(tech_name__in=tech_stack_list)
    obj.user = User.objects.get(id=request.data["user_id"])
    obj.post_title = request.data["post_title"]
    obj.post_gist = request.data["post_gist"]
    obj.post_description = request.data["post_description"]
    obj.status = request.data["status"]
    obj.save()
    obj.tech_stack.set(tech_stack_ids)
    obj.save()
    obj.file = request.data["file"]
    colab_list = request.data["collaboraters"]
    colab_list = colab_list.split(',')
    print(colab_list)
    print(settings.MEDIA_ROOT + '\post_photos')
    print(settings.MEDIA_URL)
    print(settings.BASE_DIR)
    colabs = User.objects.filter(id__in=colab_list)
    obj.collaboraters.set(colabs)
    obj.save()
    try:
        fileobj = request.data["file"]
        print(fileobj.name)
        config = load_config()
        x = str(obj.file).split('/')
        link = upload(fileobj.name, settings.MEDIA_ROOT+'\\' +
                    x[0] + '\\' + x[1], config["azure_storage_connectionstring"], config["container_name"])
        print(settings.MEDIA_ROOT+'\\' + x[0] +'\\' + x[1])
        print(obj.file)
        print(link)
        obj.image_url = link
        obj.save()
    except:
        return Response(status=202)
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
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_liked_posts(request): #gets liked posts of a user when token is given
    user = request.user
    if user.is_authenticated:
        postsobj = UserPostSerializer(user.liked_posts.all(),many=True)
        return JsonResponse(postsobj.data,safe=False)
    else:
        return Response(status=401)
@api_view(['GET'])
def post_liked_by_user(request,pk):
    user = request.user
    if user.is_authenticated:
        postobj = UserPost.objects.get(id=pk)
        if postobj in user.liked_posts.all():
            return JsonResponse({"liked" : True},safe=False)
        else:
            return JsonResponse({"liked":False},safe=False)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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


