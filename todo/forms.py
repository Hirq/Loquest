from django import forms
from .models import Quest, Choice, Victory, Purpose


class QuestForm(forms.ModelForm):
    class Meta:
        model = Quest
        fields = ['quest_name', 'quest_text', 'levels']

    def __init__(self, *args, **kwargs):
        super(QuestForm, self).__init__(*args, **kwargs)
        self.fields['quest_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'quest_name'})
        self.fields['quest_text'].widget.attrs.update({
            'class': 'form-control',
            'name': 'quest_text'})


class LogForm(forms.ModelForm):
    """LogForm"""
    class Meta:
        model = Choice
        fields = ['choice_text']

    def __init__(self, *args, **kwargs):
        super(LogForm, self).__init__(*args, **kwargs)
        self.fields['choice_text'].widget.attrs.update({
            'class': 'form-control',
            'name': 'choice_text'})


class VictoryForm(forms.ModelForm):
    class Meta:
        model = Victory
        fields = ['victory_text', 'pub_date']

    def __init__(self, *args, **kwargs):
        super(VictoryForm, self).__init__(*args, **kwargs)
        self.fields['victory_text'].widget.attrs.update({
            'class': 'form-control',
            'name': 'victory_text'})
        self.fields['pub_date'].widget.attrs.update({
            'class': 'form-control',
            'name': 'pub_date'})


class PurposeForm(forms.ModelForm):
    class Meta:
        model = Purpose
        fields = ['purpose_text', 'pub_date']

    def __init__(self, *args, **kwargs):
        super(PurposeForm, self).__init__(*args, **kwargs)
        self.fields['purpose_text'].widget.attrs.update({
            'class': 'form-control',
            'name': 'purpose_text'})
        self.fields['pub_date'].widget.attrs.update({
            'class': 'form-control',
            'name': 'pub_date'})


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Quest
        fields = ['quest_name', 'quest_text', 'levels', 'done_date', 'done_quest']

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['quest_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'quest_name'})
        self.fields['quest_text'].widget.attrs.update({
            'class': 'form-control',
            'name': 'quest_text'})
        self.fields['levels'].widget.attrs.update({
            'class': 'form-control',
            'name': 'levels'})
        self.fields['done_date'].widget.attrs.update({
            'class': 'form-control',
            'name': 'done_date'})

class UpdateFormLog(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

    def __init__(self, *args, **kwargs):
        super(UpdateFormLog, self).__init__(*args, **kwargs)
        self.fields['choice_text'].widget.attrs.update({
            'class': 'form-control',
            'name': 'choice_text'})
