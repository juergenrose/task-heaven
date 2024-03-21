from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput, Textarea, EmailInput
from django.forms import ModelForm
from . models import Task, Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]


    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



class ContactForm(forms.Form):
    name = forms.CharField(widget=TextInput)
    email = forms.EmailField(widget=EmailInput)
    message = forms.CharField(widget=Textarea)



class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content',]
        exclude = ['user',]



class EditUserForm(forms.ModelForm):
    password = None #doesen't update the password
    class Meta:
        model = User
        fields = ['username', 'email',]
        exclude = ['passeword1', 'password2']



class UpdatePictureForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}))
    class Meta:
        model = Profile
        fields = ['profile_pic',]

