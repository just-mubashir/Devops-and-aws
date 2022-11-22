from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name='sign-up'),
    path('home', views.home, name='home'),
    path('', views.home, name='home'),
    path('create-post', views.create_post, name='create-post'),
    path('chat', views.chat, name='chat'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path(
        'getMessages/<str:room>/',
        views.getMessages, name='getMessages'
    ),
]
