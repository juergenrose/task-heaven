from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm, ContactForm, TaskForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


#website startpage
def home(request):
    return render(request, 'tasks/index.html')


#About page
def about(request):
    return render(request, 'tasks/about.html')


#user register (create) page, redirect to login and sends a message if the register is successful
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account has been successfully created") #Shows the messag when the register was successful
            return redirect('login')
    context = {'RegistrationForm' : form}
    return render(request, 'tasks/register.html', context)


#user login page, if login was successfully, the user will redirect to the dashboard
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



#logs the user out
def logout(request):
    auth.logout(request)
    return redirect('home')


#the premium pricing page
def pricing (request):
    return render(request, 'tasks/pricing.html')


#support form page
@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Ticket has been successfully created. We will contact you soon.") 
            return redirect ('contact')
    else:
        form = ContactForm()
        context = {'ContactForm': form}
    return render(request, 'tasks/contact.html', context)


#the dashboard page
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'tasks/dashboard.html')


#create a Task
@login_required(login_url='login')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    form = TaskForm()
    context = {'CreateTaskForm': form}
    return render(request, 'tasks/create.html', context)