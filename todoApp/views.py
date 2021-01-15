from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

# Create your views here.

def home(request):
    return render(request,'todo/home.html')

def signupUser(request):
    if request.method == "GET":
        return render(request,'todo/signup.html',{"form":UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentTodos')
            except IntegrityError:
                return render(request,'todo/signup.html',{"form":UserCreationForm(),"error":"Username already exists"})
        else:
            return render(request,'todo/signup.html',{"form":UserCreationForm(),"error":"Passwords does not match"})


def loginUser(request):
    if request.method == "GET":
        return render(request,'todo/login.html',{"form":AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        print(user)
        if user is None:
            return render(request,'todo/login.html',{"form":AuthenticationForm(),"error":"Username and password does not match"})
        else:
            login(request,user)
            return redirect('currentTodos')

def logoutUser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


def currentTodos(request):
    return render(request,'todo/currentTodos.html')