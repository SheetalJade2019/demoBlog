from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.forms import ModelForm
# from django.contrib.auth.models import User
from .models import Post, User, user_gender_choices,user_type_choices
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
# SignUpForm inherits UserCreationForm
class SignUpForm(UserCreationForm):
    # inspect page to get password names
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    # BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
    # Dob = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    # Dob = forms.DateField(widget=forms.SelectDateWidget())
    Dob = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.SelectDateWidget(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    gender = forms.ChoiceField(widget=forms.RadioSelect,choices=user_gender_choices)
    Type = forms.ChoiceField(widget=forms.RadioSelect,choices=user_type_choices)
    
    class Meta:
        model = User
        fields =['first_name','last_name','email', 'phone','Dob','gender','Type']
        labels ={'first_name': 'First Name', 'last_name':'Last Name',
                'email':'Email'}
        widget = {
                    'first_name':forms.TextInput(attrs={'class':'form-control'}),
                    'last_name':forms.TextInput(attrs={'class':'form-control'}),
                    'email':forms.EmailInput(attrs={'class':'form-control'}),
                    }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc']
        labels = {'title': 'Title', 'desc': 'Description'}
        widget = {'title': forms.TextInput(attrs={'class':'form-control'}),
                    'desc': forms.TextInput(attrs={'class':'form-control'})}

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'phone','Dob','gender','Type']

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control'})
    )