from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Task,Category,Priority,Visit
from . forms import TaskForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
import datetime
from django.db.models import Count, Q


# Create your views here.
# Home Page
def home(request):
    visit_count = Visit.objects.count()
    return render(request, 'homepage.html',{'visit_count': visit_count})
def about(request):
    return render(request, 'about.html')
@login_required
def dashboard(request):
   
   tasks = Task.objects.filter(user=request.user)
    
    # Get the total number of tasks
   total_tasks = tasks.count()

    # Get the number of completed tasks
   completed_tasks = tasks.filter(completed=True).count()

    # Get the number of not completed tasks
   not_completed_tasks = tasks.filter(completed=False).count()

    # Calculate percentages
   if total_tasks > 0:
        completed_percentage = (completed_tasks / total_tasks) * 100
        not_completed_percentage = (not_completed_tasks / total_tasks) * 100
   else:
        completed_percentage = 0
        not_completed_percentage = 0

    # Filter task
   completed_filter = request.GET.get('completed')
    
   if completed_filter == 'true':
        tasks = Task.objects.filter(completed=True)
   elif completed_filter == 'false':
        tasks = Task.objects.filter(completed=False)
   else:
        tasks = Task.objects.filter(user=request.user)


    # Additional statistics
   overdue_tasks = tasks.filter(due_date__lt=timezone.now(),user=request.user, completed=False).count()
   today_tasks = tasks.filter(due_date=timezone.now(),user=request.user).count()
   week_tasks = tasks.filter(user=request.user,
        due_date__range=[timezone.now() - timedelta(days=timezone.now().weekday()), 
                         timezone.now() + timedelta(days=6-timezone.now().weekday())]
    ).count()
   month_tasks = tasks.filter( user=request.user,
        due_date__month=timezone.now().month,
        due_date__year=timezone.now().year
    ).count()
   uregent = tasks.filter(priority = 1, user=request.user).count()
   normal = tasks.filter(priority = 2, user=request.user).count()
   low = tasks.filter(priority = 3, user=request.user).count()
   to_do = tasks.filter(category = 1, user=request.user).count()
   personal = tasks.filter(category = 2, user=request.user).count()
   want_to_do = tasks.filter(category = 3, user=request.user).count()
   priority_list = ['Urgent','Normal','Low','To_Do','Personal','Want To Do']
   priority_num = [uregent,normal,low,to_do,personal,want_to_do]
   # Get the number of tasks by category
   task_list1 = ['Completed','Not Completed']
   task_per = [completed_tasks,not_completed_tasks]

   if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
   else:
        form = TaskForm()

   context = {
        'priority_list' : priority_list,
        'priority_num' : priority_num,
        'task_per' : task_per,
        'task_list1' : task_list1,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'not_completed_tasks': not_completed_tasks,
        'completed_percentage': completed_percentage,
        'not_completed_percentage': not_completed_percentage,
        'overdue_tasks': overdue_tasks,
        'today_tasks': today_tasks,
        'week_tasks': week_tasks,
        'month_tasks': month_tasks,
        'form': form
    }
   return render(request, 'dashboard.html', context)

@login_required
def task_list(request):
    tasks = Task.objects.filter(user = request.user).order_by('-created_at')
    # Get filter criteria from the request
    category = request.GET.get('category')
    priority = request.GET.get('priority')
    completed = request.GET.get('completed')
    date_filter = request.GET.get('date_filter')

    # Filter tasks based on the criteria
    if category:
        tasks = tasks.filter(category__category_name=category)
    if priority:
        tasks = tasks.filter(priority__name=priority)
    if completed:
        tasks = tasks.filter(completed=(completed == 'true'))
    if date_filter:
        today = timezone.now().date()
        if date_filter == 'overdue':
            tasks = tasks.filter(due_date__lt=today, completed=False)
        elif date_filter == 'today':
            tasks = tasks.filter(due_date=today)
        elif date_filter == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            tasks = tasks.filter(due_date__range=(start_of_week, end_of_week))
        elif date_filter == 'month':
            start_of_month = today.replace(day=1)
            next_month = start_of_month + timedelta(days=32)
            start_of_next_month = next_month.replace(day=1)
            tasks = tasks.filter(due_date__lt=start_of_next_month, due_date__gte=start_of_month)

    # Get all categories and priorities for the filter form
    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
        
    
    return render(request, 'task_list.html', {'tasks': tasks, 'categories': categories, 'priorities': priorities, 'form':form})
@login_required
def task_event_view(request):
    return render(request, 'task_event.html')

@login_required
def task_events(request):
    tasks = Task.objects.filter(user=request.user)
    events = []
    for task in tasks:
        color = '#3788d8'  # Default color
        if task.completed:
            color = '#00ff00'  # Green
        elif task.priority.name == 'Urgent':
            color = '#ff0000'  # Red
        elif task.priority.name == 'Normal':
            color = '#ffa500'  # Orange
        elif task.priority.name == 'Low':
            color = '#06cfee'  # Tale
        
        events.append({
            'title': task.title,
            'description': task.description,
            'start': task.due_date.isoformat(),
            'end': task.due_date.isoformat(),
            'color': color,
        })
    return JsonResponse(events, safe=False)


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request,'create_task.html',{'form':form})



@login_required
def task_update(request,task_id):
    task = get_object_or_404(Task,pk = task_id, user = request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST,request.FILES,instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
        
    return render(request,'task_update.html',{'form':form})
@login_required
def task_delete(request,task_id):
    task = get_object_or_404(Task,pk = task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    else:
        return HttpResponseBadRequest("Invalid request method.")



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user  = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})
