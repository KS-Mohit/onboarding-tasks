from django.contrib import admin
from django.urls import path
from tasks.views import task_list, task_detail, app_view

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Front-end App URL
    path('', app_view, name='app-view'),

    # API URLs 
    path('api/tasks/', task_list, name='task-list'),
    path('api/tasks/<int:pk>/', task_detail, name='task-detail'),
]

