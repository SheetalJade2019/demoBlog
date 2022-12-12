from django.contrib import admin
from django.urls import path
from Appblog import views
#from .forms import

urlpatterns = [
    #path('',views.base, name="base"),
    path('nav/',views.navbar, name="navbar"),
    path('',views.home,name="home"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('signup/',views.user_signup,name="signup"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    
    path('update_user/<int:id>',views.update_user, name="updateuser"),
    path('change_password/<int:id>',views.change_password,name="changepassword"),
    path('users_list/<int:page_no>',views.users_list,name="userslist"),

]
