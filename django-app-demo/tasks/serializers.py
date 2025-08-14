from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        # We add 'url' to the fields list and specify the lookup_field
        fields = ['url', 'id', 'title', 'description', 'completed']
        extra_kwargs = {
            'url': {'view_name': 'task-detail', 'lookup_field': 'pk'}
        }