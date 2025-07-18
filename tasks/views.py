from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone

# Create your views here.

def home(request):
  return render(request, 'home.html')

def signup(request):
  if request.method == 'GET':
    return render(request, 'signup.html', {
     'form': UserCreationForm
    })
  elif request.method == 'POST':
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
        user.save()
        login(request, user)
        return  redirect('tasks')
      except:
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Username already exists'
        })
    else:
      return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })

def signout(request):
  logout(request)
  return redirect('home')

def signin(request):
  if request.method == 'GET':
    return render(request, 'signin.html', {
      'form': AuthenticationForm
    })
  elif request.method == 'POST':
    user = authenticate(
      request, username=request.POST['username'], 
      password=request.POST['password']
      )
    
    if user == None:
      return render(request, 'signin.html', {
        'form': AuthenticationForm,
        'error': 'Username or password is incorrect'
      })
    else:
      login(request, user)
      return redirect('tasks')

def tasks(request):
  task = Task.objects.filter(user=request.user, datecompleted__isnull=True)
  return render(request, 'tasks.html', {
    'tasks': task
  })

def create_task(request):
  if request.method == 'GET':
    return render(request, 'create_task.html', {
     'form': TaskForm
    })
  elif request.method == 'POST':
    try:
      form = TaskForm(request.POST)
      new_task = form.save(commit=False)
      new_task.user = request.user
      new_task.save()
      return redirect('tasks')
    except:
      return render(request, 'create_task.html', {
        'form': TaskForm,
        'error': 'Por favor manda datos validos'
      })

def task_detail(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'GET':
    form = TaskForm(instance=task)
    return render(request, 'task_detail.html', {
      'task': task,
      'form': form
    })
  elif request.method == 'POST':
    try:
      form = TaskForm(request.POST, instance=task)
      form.save()
      return redirect('tasks')
    except:
      return render(request, 'task_detail.html', {
       'task': task,
        'form': form,
        'error': 'Error updating task'
      })
    
def complete_task(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')
  
def delete_task(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.delete()
    return redirect('tasks')