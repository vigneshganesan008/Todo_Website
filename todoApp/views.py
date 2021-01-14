from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

# Create your views here.
def signupUser(request):
    if request.method == "GET":
        return render(request,'todo/signup.html',{"form":UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentTodos')
            except IntegrityError:
                return render(request,'todo/signup.html',{"form":UserCreationForm(),"error":"Username already exists"})
        else:
            return render(request,'todo/signup.html',{"form":UserCreationForm(),"error":"Passwords does not match"})

def currentTodos(request):
    return render(request,'todo/currentTodos.html')