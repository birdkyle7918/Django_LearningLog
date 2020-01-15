"""定义learning_logs的URL"""
from django.conf.urls import url
from . import views

urlpatterns = [

    # 引导页
    url(r'^$', views.index, name='index'),

    # 预览页
    url(r'^overall/$', views.overall, name='overall'),

    # 主页
    url(r'^main/(?P<topic_id>\d+)$', views.main, name='main'),

    # 用于添加新主题的网页界面
    url(r'^new_topic/$', views.new_topic, name='new_topic'),

    # 用于添加新条目的界面
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # 用于编辑条目的界面
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

    # 用于删除条目的界面
    url(r'^delete_entry/(?P<entry_id>\d+)/$', views.delete_entry, name='delete_entry'),

    # 用于确认删除条目
    url(r'delete_entry_confirm/(?P<entry_id>\d+)/$', views.delete_entry_confirm, name='delete_entry_confirm'),

    # 用于删除主题
    url(r'delete_topic/(?P<topic_id>\d+)/$', views.delete_topic, name='delete_topic'),

    # 用于确认删除主题
    url(r'delete_topic_confirm/(?P<topic_id>\d+)/$', views.delete_topic_confirm, name='delete_topic_confirm')

]
