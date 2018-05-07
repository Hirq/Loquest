from django.contrib import admin

from .models import Quest, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'quest_name', 'quest_text', 'levels']
    inlines = [ChoiceInline]

admin.site.register(Quest, QuestAdmin)
admin.site.register(Choice)