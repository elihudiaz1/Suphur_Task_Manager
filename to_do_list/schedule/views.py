from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from django.contrib.auth.models import User
import intervals as I


def convert_to_min(hour, min, isAM):
  to_min = min
  if (isAM == 'a.m.'):
    to_min += hour*60
  else:
    to_min += hour*60 +720   #its 12 noon expressed in minutes
  return to_min


def occupiedTime(schedule):
    b = I.closed(0,0)
    
    for i in schedule:
      start = convert_to_min(i.start_time_hour, i.start_time_min, i.start_time_mode)
      end = convert_to_min(i.end_time_hour, i.end_time_min, i.end_time_mode)
      b = (I.closed(start, end)).union(b)

    return b


def availableTime(fluid_task, schedule):
    busy = occupiedTime(schedule)
    start = convert_to_min(fluid_task.between, 0, fluid_task.start_mode)
    end = convert_to_min(fluid_task.and_end_time, 0, fluid_task.end_mode)  
    available = (I.closed(start, end) - busy)
   
    return available

def convertToHour(minutes):
  if(minutes > 780):
   return int(minutes/60)-12
  else:
    return int((minutes)/60)


def convertToMin(minutes):
  return (minutes%60)


def retrieveMode(minutes):
  if minutes > 720:
    return 'p.m.'
  return 'a.m.'


def addFluid(fluid_task, schedule):
  amount_per_portion = int(convert_to_min(fluid_task.duration_of_task, 0, 'a.m.')/fluid_task.divided_into_parts)
 

  f_task = fluid_task
  schedule.remove(fluid_task)
  a = availableTime(f_task, schedule)
  print('available times: ')
  print(a)
  print('\n')

  for i in range(len(a)):
    
    up = a[i].upper
    low = a[i].lower
    opening = (up - low)
  
    if f_task.divided_into_parts <= opening:
      t = Task(
        task_type='static',
        title=f_task.title,
        content=f_task.content,
        priority_level=f_task.priority_level,
        day_of_week=f_task.day_of_week,
        date_posted=f_task.date_posted,
        author=f_task.author,
        start_time_hour=convertToHour(low),
        start_time_min=convertToMin(low),
        start_time_mode=retrieveMode(low),
        end_time_hour=convertToHour(up),
        end_time_min=convertToMin(up),
        end_time_mode=retrieveMode(up)
      )
      t.save()
    
      schedule.append(t)
    
  return schedule


def updateList(mylist): 

  mylist.sort(key=lambda x: convert_to_min(x.start_time_hour, x.start_time_min, x.start_time_mode), reverse=False)

  return mylist

def finalList(objectList):
  for task in objectList:
  
    if task.task_type == 'fluid':
      objectList = addFluid(task, objectList)
      
  return updateList(objectList)
    





"""
def updateList(mylist):
  for i in range(len(mylist)):
    min_idx = i    
    for j in range(i+1, len(mylist)):     
      if convert_to_min(mylist[min_idx].start_time_hour, mylist[min_idx].start_time_min, mylist[min_idx].start_time_mode) > convert_to_min(mylist[j].start_time_hour, mylist[j].start_time_min, mylist[j].start_time_mode ):
        min_idx = j 
    mylist[i], mylist[min_idx] = mylist[min_idx], mylist[i]
  return mylist
 """ 


def home(request):
 context = {
  'tasks' : finalList(list(Task.objects.all()))
 }
 return render(request, 'schedule/home.html', context)

def Mhome(request):
  context = {
   'tasks' : finalList(list(Task.objects.filter(day_of_week='Monday')))
  }
  return render(request, 'schedule/home.html', context)

def Thome(request):
  context = {
    'tasks' : finalList(list(Task.objects.filter(day_of_week='Tuesday')))
  }
  return render(request, 'schedule/home.html', context)

def Whome(request):
  context = {
    'tasks' : finalList(list(Task.objects.filter(day_of_week='Wednesday')))
  }
  return render(request, 'schedule/home.html', context)

def THhome(request):
  context = {
    'tasks' : finalList(list(Task.objects.filter(day_of_week='Thursday')))
  }
  return render(request, 'schedule/home.html', context)

def Fhome(request):
  context = {
    'tasks' : finalList(list(Task.objects.filter(day_of_week='Friday')))
  }
  return render(request, 'schedule/home.html', context)

def SAhome(request):
  context = {
    'tasks' : finalList(list(Task.objects.filter(day_of_week='Saturday')))
  }
  return render(request, 'schedule/home.html', context)

def SUhome(request):
  context = {
    'tasks' : finalList(list(Task.objects.filter(day_of_week='Sunday')))
  }
  return render(request, 'schedule/home.html', context)


class TaskDetailView(DetailView):
 model = Task


class TaskCreateView(CreateView):
 model = Task
 fields = ['task_type', 'title', 'content', 'priority_level', 'day_of_week', 'start_time_hour', 'start_time_min', 'start_time_mode', 'end_time_hour', 'end_time_min', 'end_time_mode']

 def form_valid(self, form):
  form.instance.author = self.request.user
  return super().form_valid(form)


class FluidTaskCreateView(CreateView):
 model = Task
 fields = ['task_type', 'title', 'content', 'day_of_week', 'duration_of_task', 'divided_into_parts', 'between', 'start_mode', 'and_end_time', 'end_mode' ]

 def form_valid(self, form):
  form.instance.author = self.request.user
  return super().form_valid(form)


class TaskUpdateView(UserPassesTestMixin, UpdateView):
 model = Task
 fields = ['title', 'content', 'priority_level', 'day_of_week', 'start_time_hour', 'start_time_min', 'start_time_mode', 'end_time_hour', 'end_time_min', 'end_time_mode']

 def form_valid(self, form):
  form.instance.author = self.request.user
  return super().form_valid(form)

 def test_func(self):
  task = self.get_object()
  if self.request.user == task.author:
   return True
  return False


class FluidTaskUpdateView(UserPassesTestMixin, UpdateView):
 model = Task
 fields = ['task_type', 'title', 'content', 'duration_of_task', 'divided_into_parts', 'between', 'start_mode', 'and_end_time', 'end_mode' ]

 def form_valid(self, form):
  form.instance.author = self.request.user
  return super().form_valid(form)

 def test_func(self):
  task = self.get_object()
  if self.request.user == task.author:
   return True
  return False


class TaskDeleteView(UserPassesTestMixin, DeleteView):
 model = Task
 success_url = '/'

 def test_func(self):
  task = self.get_object()
  if self.request.user == task.author:
   return True
  return False

def about(request):
 return render(request, 'schedule/about.html', {'title' : 'About'})

