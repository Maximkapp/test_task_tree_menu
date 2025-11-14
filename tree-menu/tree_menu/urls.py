from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_menu_view, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('projects/project1/', views.project1, name='project1'),
    path('projects/project1/project1-1/', views.project1_1, name='project1_1'),

]
