from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='debel_home'),
    path('about/', views.about, name='debel_about'),
    path('layman/', views.layman, name='debel_layman'),
    path('virtuoso/', views.virtuoso, name='debel_virtuoso'),
    path('expert/', views.expert, name='debel_expert'),
    path('laymanMusic/', views.LaymanLoadMusic, name='debel_music_layman'),
    path('virtuosoMusic/', views.VirtuosoLoadMusic, name='debel_music_virtuoso'),
    path('expertMusic/', views.ExpertLoadMusic, name='debel_music_expert')
]
