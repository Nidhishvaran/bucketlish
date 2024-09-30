from django.urls import path
from . import views 
urlpatterns = [
    path('', views.main, name='main'),
    path('registration/', views.registration, name = "registration"),
    path('clear_tasks/', views.clear_tasks, name='clear_tasks'),
    path('add/', views.add, name = 'add'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),  # Add this line
    
]