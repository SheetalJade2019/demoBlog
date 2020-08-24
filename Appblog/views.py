from django.shortcuts import render,HttpResponseRedirect
#from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.

def base(request):
    return render(request, 'Appblog/base.html')

def navbar(request):
    return render(request, 'Appblog/navbar.html')
# home
def home(request):
    posts = Post.objects.all()
    return render(request, 'Appblog/home.html',{'posts':posts})

# about
def about(request):
    return render(request, 'Appblog/about.html')
# contact
def contact(request):
    return render(request, 'Appblog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'Appblog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congrats!! You have become author')
            user=form.save()
            group = Group.objects.get(name = "Author")
            user.groups.add(group)
    else:#if request is GET or other
        form = SignUpForm()
    return render(request, 'Appblog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Successfully logged in !")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'Appblog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

# add new posts
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form= PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst=Post(title=title,desc=desc)
                pst.save()
                form=PostForm()
        else:
            form=PostForm()
        return render(request, 'Appblog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def cancel_post(request):
    form=PostForm()
    return render(request, 'Appblog/addpost.html',{'form':form})


# update posts
def update_post(request, id):
    if request.user.is_authenticated:

        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        #return HttpResponseRedirect('/dashboard/')
        pst=Post.objects.all()
        return render(request, 'Appblog/updatepost.html',{'form':form,'post':pst})
    else:
        return HttpResponseRedirect('/login/')


# delete posts
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
