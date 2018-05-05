from django.urls import path

from . import views

app_name = "todo"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('quest_form', views.new_quest, name='create_quest'),
    path('<int:quest_id>/choice_form/', views.new_log, name='create_log'),
    path('<int:pk>/quest_confirm_delete/', views.QuestDelete.as_view(), name='quest_confirm_delete'),
    path('about', views.about, name='about')
]