from django.shortcuts import render, render_to_response, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
import datetime
from .models import Quest, Choice, Victory
from .forms import QuestForm, LogForm, VictoryForm, UpdateForm
import copy


class IndexView(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'list'

    def get_queryset(self):
        """Return the last five published quests."""
        return Quest.objects.order_by('-pub_date')[:25]


class DetailView(generic.DetailView):
    model = Quest
    template_name = 'todo/detail.html'

    def index(request):
        return redirect('todo:index')


def RemoveView(request):
    return render(request, 'todo/delete_all.html')


def DailyRemoveView(request):
    return render(request, 'todo/delete_daily.html')


def VictoryRemoveView(request):
    return render(request, 'todo/delete_victory.html')


def About(request):
    return render(request, 'todo/about.html')


def NewQuest(request):
    current_user = request.user

    if request.method == "POST":
        form = QuestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.who = current_user
            post.save()

            return redirect('todo:index')
    else:
        form = QuestForm()

    return render(request, 'todo/quest_form.html', {'form': form})


def NewTodayQuest(request):
    current_user = request.user

    if request.method == "POST":
        form = QuestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.who = current_user
            post.today_quest = True
            post.save()

            return redirect('todo:index')
    else:
        form = QuestForm(initial={'today_quest': True})

    return render(request, 'todo/quest_form.html', {'form': form})


def NewLog(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    quest_text = quest.quest_text
    quest_name = quest.quest_name
    who_add = quest.who

    if request.method == "POST":
        form = LogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.quest = quest
            post.pub_date = timezone.now()
            post.save()
            return redirect('todo:index')

    else:
        form = LogForm(initial={'choice_text': 'example text'})

    return render(request, 'todo/choice_form.html', {'who': who_add, 'quest_name': quest_name, 'form': form, 'quest_text': quest_text})


class DoneQuest(UpdateView):
    model = Quest
    form_class = UpdateForm

    template_name_suffix = '_update_form'
    success_url = reverse_lazy('todo:index')

    def get_initial(self):
        return {'done_quest': True, 'done_date': timezone.now()}


class DeleteQuest(DeleteView):
    model = Quest
    success_url = reverse_lazy('todo:index')


def DeleteTodayQuestsDone(request):
    current_user = request.user
    quests = Quest.objects.filter(today_quest=True, done_quest=True, who=current_user)
    quests.delete()
    return render(request, 'todo/delete_today.html')


def DeleteTodayQuest(request):
    current_user = request.user
    quests = Quest.objects.filter(today_quest=True, done_quest=False, who=current_user)
    quests.delete()
    return render(request, 'todo/delete_today.html')


def DeleteAllQuests(request):
    current_user = request.user
    quests = Quest.objects.filter(who=current_user)
    quests.delete()
    return render(request, 'todo/confirmation.html')


class VictoryList(generic.ListView):
    template_name = 'todo/victory.html'
    context_object_name = 'victory_list'

    def get_queryset(self):
        return Victory.objects.order_by('-pub_date')[:20]


def AddVictory(request):
    current_user = request.user

    if request.method == "POST":
        form = VictoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.who = current_user
            post.pub_date = timezone.now()
            post.save()

            return redirect('todo:victory')
    else:
        form = VictoryForm()

    return render(request, 'todo/victory_form.html', {'form': form, })


def DeleteVictoriesAll(request):
    current_user = request.user

    victories = Victory.objects.filter(who=current_user)
    victories.delete()
    return render(request, 'todo/confirmation.html')


class DeleteVictory(DeleteView):
    model = Victory
    success_url = reverse_lazy('todo:victory')


# Section of daily
def DailyViewBasic(request):
    return render(request, "todo/daily.html")


class DailyList(generic.ListView):
    template_name = 'todo/daily.html'
    context_object_name = 'daily_list'

    def get_queryset(self):
        return Quest.objects.order_by('-pub_date')[:20]


def NewDailyQuest(request):
    current_user = request.user

    if request.method == "POST":
        form = QuestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.who = current_user
            post.today_quest = False
            post.daily_quest = True
            post.save()

            return redirect('todo:daily')
    else:
        form = QuestForm(initial={'today_quest': True, 'daily_quest': True})

    return render(request, 'todo/quest_form.html', {'form': form})


def CopyDailyQuests_TransportOriginal(request):
    current_user = request.user


    dailies = Quest.objects.filter(today_quest=True, done_quest=False, daily_quest=True, who=current_user)
    dailies.update(daily_quest=False)

    return render(request, 'todo/confirmation.html')


def CopyDailyQuests(request):
    current_user = request.user

    quests = Quest.objects.filter(today_quest=False, daily_quest=True, done_quest=False, who=current_user)
    daily = copy.copy(quests)
    quests.update(daily_quest=False, today_quest=True)
    for quest in daily:
        quest.pk = None
        quest.save()

    return render(request, 'todo/confirmation.html')


def DeleteDailyQuests(request):
    current_user = request.user
    quests = Quest.objects.filter(daily_quest=True, today_quest=False, done_quest=False, who=current_user)
    quests.delete()
    return render(request, 'todo/confirmation.html')
