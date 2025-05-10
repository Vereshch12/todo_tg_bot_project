from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, UserProfile, Category
from .serializers import TaskSerializer
from django.contrib.auth.models import User

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        telegram_id = self.request.query_params.get('telegram_id')
        if telegram_id:
            try:
                user_profile = UserProfile.objects.get(telegram_id=telegram_id)
                return Task.objects.filter(user=user_profile.user)
            except UserProfile.DoesNotExist:
                return Task.objects.none()
        return Task.objects.all()

    def perform_create(self, serializer):
        telegram_id = self.request.query_params.get('telegram_id')
        if not telegram_id:
            raise ValueError("telegram_id is required")
        try:
            user_profile = UserProfile.objects.get(telegram_id=telegram_id)
            # Сохраняем задачу без категорий
            task = serializer.save(user=user_profile.user)
            # Обрабатываем категории
            categories_data = self.request.data.get('categories', [])
            if categories_data:
                category_objects = []
                for category_name in categories_data:
                    if category_name.strip():  # Пропускаем пустые названия
                        category, _ = Category.objects.get_or_create(
                            user=user_profile.user,
                            name=category_name,
                            defaults={'description': ''}
                        )
                        category_objects.append(category)
                task.categories.set(category_objects)
        except UserProfile.DoesNotExist:
            raise ValueError("User with this telegram_id does not exist")

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

class LinkTelegramIDView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            existing_profile = UserProfile.objects.filter(telegram_id=telegram_id).first()
            if existing_profile:
                return Response(
                    {"message": "Telegram ID already linked to user", "username": existing_profile.user.username},
                    status=status.HTTP_200_OK
                )

            username = f"telegram_{telegram_id}"[:30]
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"telegram_{telegram_id}_{counter}"[:30]
                counter += 1
                if counter > 1000:
                    return Response({"error": "Unable to generate unique username"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=username,
                password="default_password"
            )
            profile = UserProfile.objects.create(user=user, telegram_id=telegram_id)
            return Response(
                {"message": "Telegram ID linked successfully", "username": user.username},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": f"Failed to link Telegram ID: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)