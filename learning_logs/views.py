from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.


def index(request):
    # 学习笔记的主页
    return render(request, 'learning_logs/index.html')


@login_required
def overall(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/overall.html', context)


@login_required
def main(request, topic_id):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    topic_to_view = Topic.objects.get(id=topic_id)
    if topic_to_view.owner != request.user:
        raise Http404
    entries = topic_to_view.entry_set.order_by('-date_added')    # -号指的是降序排序，笔记按照降序排序

    context = {'topics': topics, 'topic_id': topic_id, 'entries': entries, 'topic_to_view':topic_to_view}
    return render(request, 'learning_logs/main.html', context)


@login_required
def new_topic(request):
    # 添加新主题
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:overall'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)  # 第一个参数是请求类型，第二个是模板，最后一个是数据


@login_required
def new_entry(request, topic_id):
    # 在特定的主题添加新的条目
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个新的表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:main', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    # 编辑已有的条目
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 初次请求，用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:main', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    entry_to_be_deleted_id = entry_id
    entry_tobe_deleted = Entry.objects.get(id=entry_id)
    topic = entry_tobe_deleted.topic
    context = {'entry_to_be_deleted_id': entry_to_be_deleted_id, 'topic': topic}
    return render(request, 'learning_logs/delete_entry.html', context)


@login_required
def delete_entry_confirm(request, entry_id):
    entry_tobe_deleted = Entry.objects.get(id=entry_id)
    topic = entry_tobe_deleted.topic
    entry_tobe_deleted.delete()
    return HttpResponseRedirect(reverse('learning_logs:main', args=[topic.id]))


def delete_topic(request, topic_id):
    topic_to_be_deleted_id = topic_id
    topic_to_be_deleted = Topic.objects.get(id=topic_to_be_deleted_id)
    context = {'topic_to_be_deleted_id': topic_to_be_deleted_id, 'topic_to_be_deleted': topic_to_be_deleted}
    return render(request, 'learning_logs/delete_topic.html', context)


def delete_topic_confirm(request, topic_id):
    topic_tobe_deleted = Topic.objects.get(id=topic_id)
    topic_tobe_deleted.delete()
    return HttpResponseRedirect(reverse('learning_logs:overall'))
