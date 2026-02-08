from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# -----------------------------
# HTML Views
# -----------------------------

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Пароли не совпадают")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('task_list_page')

    return render(request, 'tasks/register.html')

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('task_list_page')
            else:
                messages.error(request, "Неправильный email или пароль")
        except User.DoesNotExist:
            messages.error(request, "Пользователь не найден")
    return render(request, 'tasks/login.html')

def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def task_list_page(request):
    # 1️⃣ ВСЕ задачи пользователя (НЕ ТРОГАЕМ)
    all_tasks = Task.objects.filter(owner=request.user)

    # 2️⃣ queryset для фильтрации и вывода
    tasks = all_tasks

    # ---- фильтр по статусу ----
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    # ---- фильтр по дедлайну ----
    deadline = request.GET.get('deadline')
    if deadline:
        tasks = tasks.filter(deadline=deadline)

    # ---- поиск ----
    search = request.GET.get('search')
    if search:
        tasks = tasks.filter(title__icontains=search)

    # ---- сортировка ----
    ordering = request.GET.get('ordering')
    if ordering in ['created_at', '-created_at']:
        tasks = tasks.order_by(ordering)

    # ---- пагинация ----
    page = int(request.GET.get('page', 1))
    per_page = 5
    total = tasks.count()
    start = (page - 1) * per_page
    end = start + per_page
    tasks_paginated = tasks[start:end]
    total_pages = (total + per_page - 1) // per_page

    # 3️⃣ СТАТИСТИКА — ТОЛЬКО от all_tasks
    todo_count = all_tasks.filter(status='todo').count()
    in_progress_count = all_tasks.filter(status='in_progress').count()
    done_count = all_tasks.filter(status='done').count()

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks_paginated,
        'status': status or '',
        'deadline': deadline or '',
        'search': search or '',
        'ordering': ordering or '',
        'page': page,
        'total_pages': total_pages,
        'todo_count': todo_count,
        'in_progress_count': in_progress_count,
        'done_count': done_count,
    })


@login_required
def task_detail_page(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create_page(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('task_list_page')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Создать задачу'})

@login_required
def task_update_page(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list_page')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Редактировать задачу'})

@login_required
def task_delete_page(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list_page')
    return render(request, 'tasks/task_delete.html', {'task': task})
