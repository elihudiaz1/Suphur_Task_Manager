from django.urls import path
from .views import  TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, FluidTaskCreateView, FluidTaskUpdateView
from . import views


urlpatterns = [
    path('', views.home, name='schedule-home'),
    path('monday/', views.Mhome, name='schedule-monday'),
    path('tuesday/', views.Thome, name='schedule-tuesday'),
    path('wednesday/', views.Whome, name='schedule-wednesday'),
    path('thursday/', views.THhome, name='schedule-thursday'),
    path('friday/', views.Fhome, name='schedule-friday'),
    path('saturday/', views.SAhome, name='schedule-saturday'),
    path('sunday/', views.SUhome, name='schedule-sunday'),
    path('<int:pk>/', TaskDetailView.as_view(), name='schedule-detail'),
    path('<int:pk>/staticupdate/', TaskUpdateView.as_view(), name='schedule-update'),
    path('<int:pk>/fluidupdate/', FluidTaskUpdateView.as_view(), name='schedule-update-fluid'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='schedule-delete'),
    path('newstatic/', TaskCreateView.as_view(), name='schedule-create'),
    path('newfluid/', FluidTaskCreateView.as_view(), name='schedule-create-fluid'),
    path('about/', views.about, name='schedule-about')
]