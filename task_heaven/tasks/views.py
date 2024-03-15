from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



#website startpage
def home(request):
    return render(request, 'tasks/index.html')


#contact page
def contact(request):
    return render(request, 'tasks/contact.html')


#user register (create) page
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'RegistrationForm' : form}
    return render(request, 'tasks/register.html', context)


#user login page 
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'LoginForm': form}
    return render(request, 'tasks/login.html', context)



#log the user out
def logout(request):
    auth.logout(request)
    return redirect('home')


#the premium pricing page
def pricing (request):
    return render(request, 'tasks/pricing.html')

#the about us page
def about(request):
    return render(request, 'tasks/about.html')

#the dashboard page
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'tasks/dashboard.html')