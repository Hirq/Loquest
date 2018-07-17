import django_filters
from django import forms
from todo.models import Quest, Victory, Purpose

class QuestFilter(django_filters.FilterSet):
    quest_name = django_filters.CharFilter(lookup_expr='icontains')
    pub_date_year = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='year')
    pub_date_month = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='month')
    pub_date_day = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='day')
    
    class Meta:
        model = Quest
        fields = ['quest_name','levels','done_quest', 'pub_date_year', 'pub_date_month','pub_date_day']

class VictoryFilter(django_filters.FilterSet):
    victory_text = django_filters.CharFilter(lookup_expr='icontains')
    pub_date_year = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='year')
    pub_date_month = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='month')
    pub_date_day = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='day')
    
    class Meta:
        model = Victory
        fields = ['victory_text', 'pub_date_year', 'pub_date_month','pub_date_day']

class PurposeFilter(django_filters.FilterSet):
    purpose_text = django_filters.CharFilter(lookup_expr='icontains')
    pub_date_year = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='year')
    pub_date_month = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='month')
    pub_date_day = django_filters.NumberFilter(field_name = 'pub_date', lookup_expr='day')

    class Meta:
        model = Purpose
        fields = ['purpose_text', 'pub_date_year', 'pub_date_month','pub_date_day']
