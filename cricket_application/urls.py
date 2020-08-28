from django.urls import path

from . import views

app_name = 'cricket_application'

urlpatterns = [
    path('', views.MatchesView, name='home'),
    path('schedule_match/', views.CreateMatch, name='schedule'),
    path('teams/', views.TeamList, name='team_list'),
    path('teams/<team_identifier>/', views.TeamDetailView, name='team_detail'),
    path('player_detail/<id>/', views.PlayerDetailView, name='player_detail'),
    path('save_match/', views.save_match, name='save_match'),
    path('update_match/<id>', views.update_match, name='update_match'),
    path('points_table/', views.TeamPoints, name='teamPoints'),
    path('login/', views.loginpage, name='login'),
    path('logout', views.logoutpage, name='logout'),
]
