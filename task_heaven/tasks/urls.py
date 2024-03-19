from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('features', views.features, name='features'),
    path('pricing', views.pricing, name='pricing'),
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
]