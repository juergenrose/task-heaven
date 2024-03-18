from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput, Textarea, EmailInput
from . models import Task


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class ContactForm(forms.Form):
    name = forms.CharField(widget=TextInput)
    email = forms.EmailField(widget=EmailInput)
    message = forms.CharField(widget=Textarea)


class TaskForm(forms.Form):
    class Meta:
        model = Task
        fields = '__all__'