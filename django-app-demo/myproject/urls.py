# In myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet
from tasks.views import TaskViewSet, app_view

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# The API URLs are now determined automatically by the router.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # We'll put the API under /api/ now
    path('', app_view, name='app-view'), # 2. Add this line for our main app page
]