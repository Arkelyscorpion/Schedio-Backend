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
# Create your views here.

from .forms import CreateUserForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import RegisterSerializer


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
    if user.is_authenticated:
        return Response({
            'id': user.id,
            'username': user.username,
        })
    return Response({'error': 'error'})
# def registerPage(request):
#     form = CreateUserForm()

#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         print(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')


#     context = {'form':form}
#     return render(request,'register.html',context)


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


# def loginPage(request):

#     if(request.method == 'POST'):
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request,username=username, password=password)

#         if user is not None:
#             login(request,user)
#             return redirect('home')
#     context = {}
#     return render(request,'login.html',context)


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
