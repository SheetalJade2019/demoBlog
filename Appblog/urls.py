from django.contrib import admin
from django.urls import path
from Appblog import views
#from .forms import

urlpatterns = [
    #path('',views.base, name="base"),
    path('nav/',views.navbar, name="navbar"),
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('contact/', views.contact, name="contact"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('signup/',views.user_signup,name="signup"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('addpost/',views.add_post, name="addpost"),
    path('updatepost/<int:id>',views.update_post, name="updatepost"),
    path('deletepost/<int:id>',views.delete_post, name="deletepost"),
    path('cancelpost/',views.cancel_post, name="cancelpost"),
]
