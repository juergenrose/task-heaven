from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm, ContactForm, TaskForm, EditUserForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from . models import Task

#website startpage
def home(request):
    return render(request, 'tasks/index.html')


#Features page
def features(request):
    return render(request, 'tasks/features.html')


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
            return redirect('all-tasks')
    form = TaskForm()
    context = {'CreateTaskForm': form}
    return render(request, 'tasks/create.html', context)


#my tasks page - shows all tasks
@login_required(login_url='login')
def all_tasks(request):
    current_user = request.user.id
    task = Task.objects.all().filter(user=current_user)
    context = {'AllTasks': task}
    return render(request, 'tasks/all-tasks.html', context)


# edit tasks
@login_required(login_url='login')
def edit_task(request, pk):
    try:
        task = Task.objects.get(id=pk, user=request.user) # checks if current user is equals to the request 
    except:
        return redirect('all-tasks') #if not, user get redirected to all-tasks
    
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('all-tasks')
    context = {'EditTask': form}
    return render(request, 'tasks/edit-task.html', context)


# delete task
@login_required(login_url='login')
def delete_task(request, pk):
    try:
        task = Task.objects.get(id=pk, user=request.user)
    except:
        return redirect('all-tasks')
    if request.method == 'POST':
        task.delete()
        return redirect('all-tasks')
    return render(request, 'tasks/delete-task.html')



#user management page
@login_required(login_url='login')
def user_management(request):
    form = EditUserForm(instance=request.user)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'ProfileForm': form}
    return render(request, 'tasks/user-management.html', context)