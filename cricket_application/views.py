from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate, login, logout
import itertools


def MatchesView(request):
    '''
        MatchView function is displays the match schedules details
    '''
    matches = MatchesFixture.objects.order_by('-match_date')
    allteams = CricketTeam.objects.all()
    context = {
        'matches': matches,
        'allteams': allteams
    }
    return render(request, 'matches/match_fixture.html', context)


@unauthenticated_user
def CreateMatch(request):
    '''
        CreateMatch function is used to schedule a matches between two teams.Schedules are created by admin person
    '''
    allteams = CricketTeam.objects.all()
    allvenues = MatchVenues.objects.all()
    venuelist = []
    for venue in allvenues:
        venuelist.append(venue.stadium_name + ',' + venue.stadium_city)
    match_between_teams = []
    match_possibilities = itertools.combinations(allteams, 2)
    for teams in match_possibilities:
        match_between_teams.append((teams[0].team_name, teams[1].team_name))
    context = {'match_teams': match_between_teams, 'venues': venuelist}
    return render(request, 'matches/match_create_form.html', context)


def save_match(request):
    '''
        save_match function is used to save the scheduled matches into ddtabase
    '''
    teams = request.POST['Teams']
    match_venue = request.POST['venue']
    match_date = request.POST['match_date']
    allteams = CricketTeam.objects.all()
    for team in teams.split(", "):
        if '(' in team:
            team1 = team.replace("(", "")
            team1 = team1[1:-1]
        elif ')' in team:
            team2 = team.replace(")", "")
            team2 = team2[1:-1]
    for playing_team in allteams:
        if playing_team.team_name == team1:
            team1_logo = playing_team.team_logo
        elif playing_team.team_name == team2:
            team2_logo = playing_team.team_logo
    schedule = MatchesFixture(playing_team1=team1, playing_team2=team2, match_venue=match_venue, match_date=match_date,
                              playing_team1_logo=team1_logo, playing_team2_logo=team2_logo)
    schedule.save()
    return redirect('cricket_application:home')


def TeamList(request):
    '''
        TeamList function is displays the list of teams
    '''
    teams = CricketTeam.objects.all()
    context = {'teams': teams}
    return render(request, 'teams/team_list.html', context)


def TeamDetailView(request, team_identifier):
    '''
        TeamDetailView function is displays the players of perticular team
    '''
    try:
        team = CricketTeam.objects.get(team_identifier__iexact=team_identifier)
        context = {'team': team}
        return render(request, 'teams/team_detail.html', context)
    except ObjectDoesNotExist:
        messages.info(request, 'Page Not Found')
        return redirect('cricket_application:team_list')


def PlayerDetailView(request, id):
    '''
        PlayerDetailView function is displays the player history
    '''
    try:
        object = PlayerHistory.objects.get(player_id=id)
        team=object.player.teams.team_name
        team = CricketTeam.objects.get(team_name=team)
        context = {'team': team, 'object': object}
        return render(request, 'players/player_detail.html', context)
    except ObjectDoesNotExist:
        messages.info(request, 'Add Player Details')
        return render(request, 'players/player_detail.html')


def TeamPoints(request):
    '''
        TeamPoints function is get the points of teams automatically based on the matches fixtures
    '''
    pts_table_teams = Points.objects.all()
    allteams = CricketTeam.objects.all()
    total_matches_scheduled = MatchesFixture.objects.all().count()
    matches_not_com = MatchesFixture.objects.filter(match_winner=None).count()
    matches_compleated = MatchesFixture.objects.exclude(match_winner=None)
    teams_list = set()
    for each_team in allteams:
        teams_list.add(each_team.team_name)
    for team in teams_list:
        tab_team, created = Points.objects.get_or_create(team=team)
    for team in pts_table_teams:
        matches_played = matches_compleated.filter(playing_team1=team).count() + matches_compleated.filter(
            playing_team2=team).count()
        matches_own = matches_compleated.filter(match_winner=team).count()
        matches_tied = matches_compleated.filter(match_winner__iexact='Tied').count()
        matches_lost = matches_played - matches_own - matches_tied
        points = matches_played + matches_own - matches_lost

        tab_update = pts_table_teams.get(team=team)
        tab_update.matches_played = matches_played
        tab_update.matches_won = matches_own
        tab_update.matches_tied = matches_tied
        tab_update.matches_lost = matches_lost
        tab_update.points = points
        tab_update.save()
        return render(request, 'teams/team_points.html', {'points': pts_table_teams})
    return render(request, 'teams/team_points.html', {'points': pts_table_teams})


def update_match(request, id):
    '''
        update_match function is created for update the winner of the match
    '''
    match = MatchesFixture.objects.get(id=id)
    if request.method == 'POST':
        match.match_winner = request.POST.get('win')
        match.save()
        messages.success(request, 'Winner Updated Successfully')
        return redirect('/')
    else:
        return render(request, 'matches/update_match_winner.html', {'match': match})


def loginpage(request):
    '''
        loginpage function is created to authenticated persons only can add the teams,players,schedules etc..
    '''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cricket_application:schedule')
        else:
            messages.warning(request, 'Username Or Password Wrong')
    return render(request, 'account/loginpage.html')


def logoutpage(request):
    '''
        logout function is created to logout after creating the required detaills
    '''
    logout(request)
    return redirect('cricket_application:home')
