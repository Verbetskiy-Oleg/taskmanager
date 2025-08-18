from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "completed"]
        labels = {
            "title": "Название",
            "description": "Описание",
            "completed": "Выполнено",
        }
