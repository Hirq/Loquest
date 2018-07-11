import django_filters
from django import forms
from todo.models import Quest

class QuestFilter(django_filters.FilterSet):
    quest_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Quest
        fields = ['quest_name','levels','done_quest']
        