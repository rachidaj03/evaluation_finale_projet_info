from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('signin/', views.signin, name="submit_signin"),
    path('gestion_clientele/',views.gestion_clientele,name="gestion_clientele"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('create_object_1',views.create_new_object_1,name='create_object_1'),
    path('remove_object_3',views.remove_object_3,name='remove_object_3'),
    path('remove_object_4',views.remove_object_4,name='remove_object_4'),
    path('transition_1',views.transition_1,name='transition_1'),
    path('transition_2',views.transition_2,name='transition_2'),
    path('modifier_3',views.modifier_3,name='modifier_3'),
    path('modifier_4',views.modifier_4,name='modifier_4'),
    path('modifier_5',views.modifier_5,name='modifier_5'),
    path('calendar/',views.calendar,name="calendar"),
    path('webhook/', views.webhook, name='messenger_webhook'),
    path('send_message/', views.send_message, name='send_message'),
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('interactions/', views.interactions, name='interactions'),
    path('suivi_ventes/', views.suivi_ventes, name='suivi_ventes'),
]