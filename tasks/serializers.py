from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

# Для регистрации пользователя
class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Пароль должен быть минимум 8 символов")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

# Для задач
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # только для чтения

    class Meta:
        model = Task
        fields = '__all__'
