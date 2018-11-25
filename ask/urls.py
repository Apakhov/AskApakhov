from django.urls import path

from . import views

app_name = 'ask'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_num>/', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('hot/<int:page_num>/', views.hot, name='hot'),
    path('ask/', views.ask, name='ask'),
    path('signup/', views.signup, name='signup'),
    path('question/', views.page404, name='question'),
    path('question/<int:question_num>/', views.question, name='question'),
    path('settings/', views.settings, name='settings'),
    path('tag/<tag>/', views.tagged, name='tagged'),
    path('tag/<tag>/<int:page_num>/', views.tagged, name='tagged'),
]