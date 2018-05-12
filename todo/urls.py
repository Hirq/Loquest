from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "todo"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('quest_form', views.new_quest, name='create_quest'),
    path('<int:quest_id>/choice_form/', views.new_log, name='create_log'),
    path('<int:pk>/quest_confirm_delete/', views.QuestDelete.as_view(), name='quest_confirm_delete'),
    path('about', views.about, name='about'),
    path('<int:pk>/quest_update_form/', views.DoneQuest.as_view(), name='quest_update_form'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)