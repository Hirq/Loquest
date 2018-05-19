from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "todo"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('about', views.About, name='about'),

    path('quest_form', views.NewQuest, name='create_quest'),
    path('quest_form_today', views.NewTodayQuest, name='create_quest_today'),
    path('<int:quest_id>/choice_form/', views.NewLog, name='create_log'),
    path('<int:pk>/quest_update_form/', views.DoneQuest.as_view(), name='quest_update_form'),

    path('<int:pk>/quest_confirm_delete/', views.DeleteQuest.as_view(), name='quest_confirm_delete'),
    path('delete_today_quest_done', views.DeleteTodayQuestsDone, name='delete_today_quests_done'),
    path('delete_all_quests', views.DeleteAllQuests, name='delete_all_quests'),
    path('delete_view', views.RemoveView, name='delete_view'),
    path('delete_today_quests', views.DeleteTodayQuest, name='delete_today_quests'),

    path('victory', views.VictoryList.as_view(), name='victory'),
    path('victory/victory_form', views.AddVictory, name='victory_form'),
    path('victory_delete_all', views.DeleteVictoriesAll, name='victory_delete_all'),
    path('<int:pk>/victory/victory_confirm_delete/', views.DeleteVictory.as_view(), name='victory_confirm_delete')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)