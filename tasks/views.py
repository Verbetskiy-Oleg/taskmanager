from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Task

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Теперь можно войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'tasks/task_form.html')
