from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import UserRegisterForm, TaskForm
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


@login_required
def task_list(request):
    # Базовая выборка только своих задач
    qs = Task.objects.filter(user=request.user)

    # Поиск
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    # Фильтр статуса (optional)
    status = request.GET.get('status')
    if status == 'done':
        qs = qs.filter(is_done=True)
    elif status == 'pending':
        qs = qs.filter(is_done=False)

    # Сортировка
    sort = request.GET.get('sort', '-due_date')  # дефолт: ближайшие наверху
    allowed = {
        'title': 'title',
        '-title': '-title',
        'due_date': 'due_date',
        '-due_date': '-due_date',
        'status': 'is_done',
        '-status': '-is_done',
    }
    order_by = allowed.get(sort, '-due_date')
    qs = qs.order_by(order_by)

    context = {
        'tasks': qs,
        'q': q,
        'status': status or '',
        'sort': sort,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Задача создана.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача обновлена.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})
