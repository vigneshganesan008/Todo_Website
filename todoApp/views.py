from todoApp.models import Todo
from todoApp.forms import TodoForm
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render , get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.utils import timezone

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
        if user is None:
            return render(request,'todo/login.html',{"form":AuthenticationForm(),"error":"Username and password does not match"})
        else:
            login(request,user)
            return redirect('currentTodos')

def logoutUser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


def createTodos(request):
    if request.method == "GET":
        return render(request,'todo/createTodos.html',{"form":TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request,'todo/createTodos.html',{"form":TodoForm(),"error":"Enter a proper value."})

def currentTodos(request):
    todos= Todo.objects.filter(user = request.user,completed__isnull = True)
    return render(request,'todo/currentTodos.html',{"todos":todos})

def completedTodos(request):
    todos= Todo.objects.filter(user = request.user,completed__isnull = False)
    return render(request,'todo/completedTodos.html',{"todos":todos})

def viewTodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk, user = request.user)
    if request.method == "GET":
        form = TodoForm(instance= todo)
        return render(request,'todo/viewTodo.html',{"todo":todo,"form":form})
    else: 
        try:
            newtodo = TodoForm(request.POST,instance=todo)
            newtodo.save()   
            return redirect("currentTodos")
        except ValueError:
            return render(request,'todo/viewTodo.html',{"todo":todo,"form":TodoForm(instance= todo),"error":"Enter valid data"})

def completeTodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk, user = request.user)
    if request.method == "POST":
        todo.completed= timezone.now()
        todo.save()
        return redirect("currentTodos")

def deleteTodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk, user = request.user)
    if request.method == "POST":
        todo.delete()
        return redirect("currentTodos")
