from django import forms
from .models import Quest, Choice

class QuestForm(forms.ModelForm):

    class Meta:
        model = Quest
        fields = ['quest_name', 'quest_text']


class LogForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['quest', 'choice_text']

