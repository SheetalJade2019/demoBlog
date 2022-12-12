from django.shortcuts import render,HttpResponseRedirect
#from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm, PostForm, UserForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post, User
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
import math
# Create your views here.

def base(request):
    return render(request, 'Appblog/base.html')

def navbar(request):
    return render(request, 'Appblog/navbar.html')
# home
def home(request):
    posts = Post.objects.all()
    return render(request, 'Appblog/home.html',{'posts':posts})

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        # posts=Post.objects.all()
        users = User.objects.all()
        user = request.user
        profile = {
            "user_id":user.User_ID,
            "fist_name":user.first_name,
            'last_name':user.last_name,
            'email':user.email, 
            'phone':user.phone,
            'Dob':user.Dob,
            'gender':user.gender,
            'Type':user.Type
            }
        full_name = user.get_full_name()
        # gps = user.groups.all()
        return render(request, 'Appblog/dashboard.html',{'profile':profile,'full_name':full_name,'groups':"gps",'users':users, "user":user})
        # return render(request, 'Appblog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps,'users':users})
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
            return HttpResponseRedirect('/login/')
            # group = Group.objects.get(name = "Author")
            # user.groups.add(group)
    else:#if request is GET or other
        form = SignUpForm()
    return render(request, 'Appblog/home.html',{'form':form, "register_req":True})

def user_login(request):
    print("REQUEST DATA : ",request.POST)
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
        return render(request, 'Appblog/home.html',{'form':form, "login_req":True})
    else:
        return HttpResponseRedirect('/dashboard/')


# update posts
def update_user(request, id):
    if request.user.is_authenticated:
        print("__________________________________________",type(id))
        user = User.objects.get(User_ID=int(id))
        if request.method == "POST":
            pi = User.objects.get(User_ID=int(id))
            print(pi.User_ID)
            form = UserForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = User.objects.get(User_ID=id)
            print(pi.User_ID)
            form = UserForm(instance=pi)
        #return HttpResponseRedirect('/dashboard/')
        # user=User.objects.all()
        # print({'form':form,'user':user})
        return render(request, 'Appblog/dashboard.html',{'form':form,'user':user, "updateUser":True})
    else:
        return HttpResponseRedirect('/login/')


def change_password(request,id):
    print("REQUEST DATA : ",request.POST)

    if request.user.is_authenticated:
        form = ChangePasswordForm()
        if request.method == "POST":
            # form = LoginForm(request=request,data=request.POST)
            email = request.POST['email']
            old_pass = request.POST['old_password']
            new_pass = request.POST['new_password']
            obj = User.objects.get(User_ID=int(id))
            user=authenticate(username=email, password=old_pass)
            if user is not None:
                # obj = User.objects.get(email=email,User_ID=id)
                obj.set_password(new_pass)
                obj.save()
                messages.success(request,'Password Updated Successfully!')
                # return HttpResponseRedirect('/dashboard/')
                return render(request, 'Appblog/dashboard.html',{"changePassword":True})

            else:
                form = ChangePasswordForm()
                messages.error(request,'Username & old password did not match')
                # return HttpResponseRedirect('/dashboard/')
            return render(request, 'Appblog/dashboard.html',{"changePassword":True,"form":form})
        return render(request, 'Appblog/dashboard.html',{"changePassword":True,"form":form})
        
    messages.error(request,'Please login')
    form = LoginForm()
    return render(request, 'Appblog/home.html',{'form':form, "login_req":True})
    # return HttpResponseRedirect('')


def users_list(request,page_no):
    max_rows = 5
    if request.user.is_authenticated:
        if request.method == "GET":
            users=User.objects.all()
            clause_list=users
            max_count = math.ceil(len(clause_list)/max_rows)
                # if int(page_no) > max_count:
                #     return Response({"message":"messages['build_list_pageNo_incorrect']"},status=status.HTTP_400_BAD_REQUEST)
            paginator = Paginator(clause_list, max_rows)
            # pages_no = request.GET.get('page')
            pages_no = page_no
            page = paginator.page(pages_no)

            context = {"users":page.object_list,"max_page_count":max_count,"max_record_count":len(clause_list),"userList":True}
            return render(request, 'Appblog/dashboard.html',context)
