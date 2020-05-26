from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index.html', views.index, name="index"),
    path("ask", views.ask, name="ask"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path('question/<int:question_id>', views.question, name="question"),
    path('registration', views.registration, name="registration"),
    path('tag/<str:tag_name>', views.tag, name="tag"),
    path('setting', views.user_setting, name="setting"),
    path('hot', views.hot, name="hot")
]
