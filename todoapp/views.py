from django.shortcuts import render
from .models import Task
from .forms import TaskForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from user_agents import parse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.html import mark_safe

def index(request):
    tasks = Task.objects.all()
    form = TaskForm()
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    return render(request, 'index.html', {'tasks': tasks, 'form': form, 'browser': parse(user_agent).browser.family })

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Use mark_safe to prevent HTML escaping
            form.save()
    return redirect('index')

def toggle_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('index')

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        old_description = task.description
        new_description = request.POST.get('description')
        task.description = new_description
        task.save()
        return JsonResponse({'message': f'Task updated from [{old_description}] to [{new_description}] successfully. The secret keyword for this question is ravenousram'})

    return JsonResponse({'message': 'POST requests are only accepted to edit tasks at this endpoint'}, status=400)