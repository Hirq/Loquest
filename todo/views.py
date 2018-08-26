from django.shortcuts import render, render_to_response, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
import datetime
from .models import Quest, Choice, Victory, Purpose
from .forms import QuestForm, LogForm, VictoryForm, UpdateForm, PurposeForm, UpdateFormLog
import copy
from django.contrib.auth.decorators import login_required
from .filters import QuestFilter, VictoryFilter, PurposeFilter


class IndexView(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'list'

    def get_queryset(self):
        """Return the last five published quests."""
        return Quest.objects.order_by('-pub_date')[::]


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            q_done = Quest.objects.filter(done_quest=True,today_quest=False, daily_quest=False, who=self.request.user).count()
            q_list = Quest.objects.filter(done_quest=False,today_quest=False,daily_quest=False,who=self.request.user).count()
            if q_list>0:
                context['list_quests'] = q_list
            if q_done>0:
                context['done_list'] = q_done
            

        return context

class DetailView(generic.DetailView):
    model = Quest
    template_name = 'todo/detail.html'
      
    def index(self, request):
        return redirect('todo:index')


def RemoveView(request):
    return render(request, 'todo/delete_all.html')


def About(request):
    return render(request, 'todo/about.html')

@login_required()
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

@login_required()
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


class UpdateLog(UpdateView):
    model = Choice
    form_class = UpdateFormLog

    template_name_suffix = '_update_log_form'
    success_url = reverse_lazy('todo:index')


class DeleteQuest(DeleteView):
    model = Quest
    success_url = reverse_lazy('todo:index')


class DeleteLog(DeleteView):
    model = Choice
    success_url = reverse_lazy('todo:index')


@login_required()
def DeleteTodayQuestsDone(request):
    current_user = request.user
    quests = Quest.objects.filter(today_quest=True, done_quest=True, who=current_user)
    quests.delete()
    return render(request, 'todo/delete_today.html')


@login_required()
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






#Victory
class VictoryList(generic.ListView):
    template_name = 'todo/victory.html'
    context_object_name = 'victory_list'

    def get_queryset(self):
        return Victory.objects.order_by('-pub_date')[:20]

@login_required()
def AddVictory(request):
    current_user = request.user

    if request.method == "POST":
        form = VictoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.who = current_user
            post.save()

            return redirect('todo:victory')
    else:
        form = VictoryForm(initial={'pub_date': timezone.now()})


    return render(request, 'todo/victory_form.html', {'form': form, })


@login_required()
def VictoryRemoveView(request):
    return render(request, 'todo/delete_victory.html')


@login_required()
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

@login_required()
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


@login_required()
def CopyDailyQuests_TransportOriginal(request):
    current_user = request.user


    dailies = Quest.objects.filter(today_quest=True, done_quest=False, daily_quest=True, who=current_user)
    dailies.update(daily_quest=False)

    return render(request, 'todo/confirmation.html')


@login_required()
def CopyDailyQuests(request):
    current_user = request.user

    quests = Quest.objects.filter(today_quest=False, daily_quest=True, done_quest=False, who=current_user)
    daily = copy.copy(quests)
    quests.update(daily_quest=False, today_quest=True)
    for quest in daily:
        quest.pk = None
        quest.save()

    return render(request, 'todo/confirmation.html')

@login_required()
def DailyRemoveView(request):
    return render(request, 'todo/delete_daily.html')


@login_required()
def DeleteDailyQuests(request):
    current_user = request.user
    quests = Quest.objects.filter(daily_quest=True, today_quest=False, done_quest=False, who=current_user)
    quests.delete()
    return render(request, 'todo/confirmation.html')








# Section Purpose
def PurposeBaseView(request):
    return render(request, "todo/purpose.html")


class PurposeList(generic.ListView):
    template_name = 'todo/purpose.html'
    context_object_name = 'purpose_list'

    def get_queryset(self):
        return Purpose.objects.order_by('-pub_date')[:20:1]



    def get_context_data(self, **kwargs):
        context = super(PurposeList, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            date_over = Purpose.objects.filter(pub_date__lte=timezone.now())
            date_over_count = Purpose.objects.filter(pub_date__lte=timezone.now()).count()
            date_tocome = Purpose.objects.filter(pub_date__gt=timezone.now())
            date_tocome_count = Purpose.objects.filter(pub_date__gt=timezone.now()).count()

            context['count_over'] = date_over_count
            context['count_tocome'] = date_tocome_count
            context['list_over'] = date_over.order_by('pub_date')[::-1]
            context['list_tocome'] = date_tocome.order_by('pub_date')[::1]
        return context


@login_required()
def AddPurpose(request):
    if request.method == "POST":
        form = PurposeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.who = request.user
            post.save()

            return redirect('todo:purpose')
    else:
        form = PurposeForm(initial={'pub_date': timezone.now()})

    return render(request, 'todo/purpose_form.html', {'form': form})


@login_required()
def PurposeRemoveView(request):
    return render(request, 'todo/delete_purpose.html')


@login_required()
def DeletePurposeAll(request):
    current_user = request.user

    Purposes = Purpose.objects.filter(who=current_user)
    Purposes.delete()
    return render(request, 'todo/confirmation.html')


class DeletePurpose(DeleteView):
    model = Purpose
    success_url = reverse_lazy('todo:purpose')

@login_required()
def search(request):
    quest_list = Quest.objects.filter(who=request.user, today_quest=False, daily_quest=False)
    quest_filter = QuestFilter(request.GET, queryset=quest_list)
    return render(request, 'todo/search.html', {'filter': quest_filter})

def search_victory(request):
    victory_list = Victory.objects.filter(who=request.user)
    victory_filter = VictoryFilter(request.GET, queryset=victory_list)
    return render(request, 'todo/search_victory.html', {'filter': victory_filter})

def search_purpose(request):
    purpose_list = Purpose.objects.filter(who=request.user)
    purpose_filter = PurposeFilter(request.GET, queryset=purpose_list)
    return render(request, 'todo/search_purpose.html', {'filter': purpose_filter})

     