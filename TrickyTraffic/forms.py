from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm


# Custom user registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(error_messages={'invalid': 'Please enter a valid email address.'})
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


# Custom login form that inherits from UserLoginForm
class CustomLoginForm(UserLoginForm):
    pass
