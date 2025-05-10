from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'created_at', 'updated_at', 'due_date', 'categories', 'completed', 'notified']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'due_date': {'required': False},
            'categories': {'required': False},
            'completed': {'required': False}
        }