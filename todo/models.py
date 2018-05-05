from django.db import models
from django.urls import reverse
from django.utils import timezone
class Quest(models.Model):

    quest_name = models.CharField(max_length=400, default='Quest')
    quest_text = models.TextField(max_length=2100)
    pub_date = models.DateTimeField('date published')

    def get_absolute_url(self):
        return reverse('todo:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.quest_name

    def __unicode__(self):
        return u"%s %s %s" % (self.quest_name, self.quest_text, self.pub_date)

class Choice(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, null=True)
    choice_text = models.TextField(max_length=2100)

    def get_absolute_url(self):
        return reverse('todo:index')

    def __str__(self):
        return self.choice_text

