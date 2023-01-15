# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory


def loginPage(request):
    context = {}
    return render(request,'login.html',context)

def registerPage(request):
    context = {}
    return render(request,'register.html',context)

def homePage(request):
    context = {}
    return render(request,'home.html')