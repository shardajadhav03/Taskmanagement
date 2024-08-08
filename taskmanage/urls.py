from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('about/',views.about,name='about'),
    path('create_task/',views.create_task,name='create_task'),
    path('task_list/',views.task_list,name='task_list'),
    path('<int:task_id>/task_update/',views.task_update,name='task_update'),
    path('<int:task_id>/task_delete/',views.task_delete,name='task_delete'),
    path('calendar/', views.task_event_view, name='task_event_view'),
    path('api/task_events/', views.task_events, name='task_events'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),

]
