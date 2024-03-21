from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm, ContactForm, TaskForm, EditUserForm, UpdatePictureForm
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages 
from . models import Task, Profile
from django.core.mail import send_mail
from django.conf import settings

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
            current_user = form.save(commit=False)
            form.save()
            send_mail("Welcome to Task Heaven!", "Congratulations, you successfully created your account", settings.DEFAULT_FROM_EMAIL, [current_user.email])
            profile = Profile.objects.create(user=current_user)
            messages.success(request, "Account has been successfully created") #Shows the message when the register was successful
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
    profile_pic = Profile.objects.get(user=request.user)
    context = {'ProfilePic': profile_pic}
    return render(request, 'tasks/dashboard.html', context)



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
    profile = Profile.objects.get(user=request.user)
    form_2 = UpdatePictureForm(instance=profile)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        form_2 = UpdatePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        if form_2.is_valid():
            form_2.save()
            return redirect('dashboard')
    context = {'UserUpdateForm': form, 'PictureUpdateForm': form_2}
    return render(request, 'tasks/user-management.html', context)



#delete user account
@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        deleteUser = User.objects.get(username=request.user)
        deleteUser.delete()
        return redirect('home')
    return render(request, 'tasks/delete-account.html')



#reset password
@login_required(login_url='login')
def PasswordResetView(request):
    form = PasswordResetForm()
    context = {'PasswordForm': form}
    return render(request, 'tasks/password-reset.html', context)