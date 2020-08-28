from django.db import models
from django_countries.fields import CountryField


class CricketTeam(models.Model):
    '''
    CricketTeam model class is created to store Teams
    '''
    team_identifier = models.CharField(max_length=10, unique=True)
    team_name = models.CharField(max_length=100)
    team_logo = models.ImageField(upload_to='team_logo')
    club_state = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.team_name


class CricketPlayer(models.Model):
    '''
        CricketPlayer model class is created to store players
    '''
    player_id = models.IntegerField(primary_key=True)
    teams = models.ForeignKey(CricketTeam, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    player_image = models.ImageField(upload_to='players')
    jersey_number = models.PositiveIntegerField(unique=True)
    country = CountryField(multiple=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class PlayerHistory(models.Model):
    '''
        PlayerHistory model class is created to store player details
    '''
    player = models.OneToOneField(CricketPlayer, on_delete=models.CASCADE)
    matches_played = models.PositiveIntegerField()
    total_runs = models.PositiveIntegerField()
    highest_score = models.PositiveIntegerField()
    fifties = models.PositiveIntegerField()
    hundreds = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.player.first_name

    class Meta:
        verbose_name = "PlayerHistory"
        verbose_name_plural = "PlayerHistory"


class MatchesFixture(models.Model):
    '''
        MatchesFixture model class is created to store match schedule details
    '''
    playing_team1 = models.CharField(max_length=100)
    playing_team2 = models.CharField(max_length=100)
    playing_team1_logo = models.ImageField()
    playing_team2_logo = models.ImageField()
    match_venue = models.CharField(max_length=100)
    match_date = models.DateTimeField()
    match_winner = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.match_winner


class Points(models.Model):
    '''
        Points model class is created to store team points details
    '''
    team = models.CharField(max_length=100)
    matches_played = models.PositiveIntegerField(default=0)
    matches_won = models.PositiveIntegerField(default=0)
    matches_lost = models.PositiveIntegerField(default=0)
    matches_tied = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.team

    class Meta:
        verbose_name = 'Points'
        verbose_name_plural = 'Points'


class MatchVenues(models.Model):
    '''
        MatchVenues model class is created to store match location details
    '''
    stadium_name = models.CharField(max_length=100)
    stadium_city = models.CharField(max_length=100)

    def __str__(self):
        return self.stadium_name

    class Meta:
        verbose_name = "MatchVenues"
        verbose_name_plural = "MatchVenues"
