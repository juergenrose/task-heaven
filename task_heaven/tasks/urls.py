from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('features', views.features, name='features'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create', views.create_task, name='create'),
    path('all-tasks', views.all_tasks, name='all-tasks'),
    path('edit-task/<str:pk>', views.edit_task, name='edit-task'),
    path('delete-task/<str:pk>', views.delete_task, name='delete-task'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('delete-account', views.delete_account, name='delete-account'),
    path('user-management', views.user_management, name='user-management'),



    #password management

    #receive password reset link
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='tasks/password-reset.html'), name='reset_password'),

    #success message - password reset was sent to email
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='tasks/password-reset-sent.html'), name='password_reset_done'), 

    #link for password reset
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='tasks/password-reset-form.html'), name='password_reset_confirm'), 

    #success message - password was successfully reset
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='tasks/password-reset-complete.html'), name='password_reset_complete'), 
]

