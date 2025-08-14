# In tasks/views.py
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import render

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer



def app_view(request):
    """This view serves the main single-page application."""
    return render(request, 'task_list.html')