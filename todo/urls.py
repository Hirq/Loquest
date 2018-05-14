from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "todo"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('quest_form', views.new_quest, name='create_quest'),
    path('quest_form_today', views.new_quest_today, name='create_quest_today'),

    path('<int:quest_id>/choice_form/', views.new_log, name='create_log'),
    path('<int:pk>/quest_confirm_delete/', views.QuestDelete.as_view(), name='quest_confirm_delete'),

    path('<int:pk>/quest_update_form/', views.DoneQuest.as_view(), name='quest_update_form'),
    path('today_delete', views.TodayDelete, name='today_delete'),
    path('delete_all', views.DeleteAll, name='delete_all'),

  path('about', views.about, name='about'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)