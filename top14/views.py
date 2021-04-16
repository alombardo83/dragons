from django.shortcuts import render
from datetime import datetime
from .models import Season, Match, Team, ROUNDS
from . import helpers


def index(request):
    template_name = 'top14/index.html'
    season = Season.objects.filter(active=True).get()

    ranking = {}
    teams = Team.objects.filter(active=True).all()
    for t in teams:
        ranking[t.id] = TeamDisplay(t)

    display_matches = []
    active_round = 1
    for num_round, name_round in ROUNDS:
        round_matches = {
            'round': num_round,
            'round_name': name_round,
            'matches': []
        }

        matches = Match.objects.filter(season__id=season.id, round=num_round).all()
        for match in matches:
            m = MatchDisplay(match)
            round_matches['matches'].append(m)
            if m.played:
                active_round = num_round
                team1 = ranking[match.team1.id]
                team2 = ranking[match.team2.id]
                team1._compute_match_results(m.score_team1, m.score_team2, m.bonus_offensive_team1,
                                             m.bonus_defensive_team1, m.withdrawn_team1, match.tries1, match.tries2)
                team2._compute_match_results(m.score_team2, m.score_team1, m.bonus_offensive_team2,
                                             m.bonus_defensive_team2, m.withdrawn_team2, match.tries2, match.tries1)

        display_matches.append(round_matches)

    ranking = helpers.sort_ranking(list(ranking.values()))
    return render(request, template_name,
                  {'matches': display_matches, 'ranking': ranking, 'active_round': active_round - 1})


class TeamDisplay:
    id = 0
    name = ''
    last_ranking = 0
    nb_points = 0
    nb_points_direct = 0
    nb_played = 0
    nb_won = 0
    nb_draw = 0
    nb_lost = 0
    nb_bonus_offensive = 0
    nb_bonus_defensive = 0
    nb_withdrawn = 0
    diff = 0
    diff_direct = 0
    nb_tries_marked = 0
    nb_tries_conceded = 0
    nb_tries_direct = 0
    diff_tries = 0
    nb_total_score = 0

    def __init__(self, team):
        self.id = team.id
        self.name = team.name
        self.nb_points -= team.penalty_points
        self.last_ranking = team.last_ranking

    def _compute_match_results(self, score1, score2, bonus_offensive, bonus_defensive, withdrawn, tries1, tries2):
        self.nb_played += 1
        self.diff += (score1 - score2)
        self.nb_tries_marked += tries1
        self.nb_tries_conceded += tries2
        self.diff_tries += (tries1 - tries2)
        self.nb_total_score += score1

        if score1 > score2:
            self.nb_won += 1
            self.nb_points += 4
        elif score1 < score2:
            self.nb_lost += 1
            self.nb_points += 0
        else:
            self.nb_draw += 1
            self.nb_points += 2

        if bonus_offensive:
            self.nb_bonus_offensive += 1
            self.nb_points += 1

        if bonus_defensive:
            self.nb_bonus_defensive += 1
            self.nb_points += 1

        if withdrawn:
            self.nb_withdrawn += 1


class MatchDisplay:
    match = None
    date_time = datetime.today()
    name_team1 = ''
    name_team2 = ''
    short_name_team1 = ''
    short_name_team2 = ''
    score_team1 = 0
    score_team2 = 0
    bonus_offensive_team1 = False
    bonus_defensive_team1 = False
    bonus_offensive_team2 = False
    bonus_defensive_team2 = False

    def __init__(self, match):
        self.match = match
        self.name_team1 = match.team1.name
        self.name_team2 = match.team2.name
        self.short_name_team1 = match.team1.short_name
        self.short_name_team2 = match.team2.short_name
        self.score_team1 = helpers.calculate_score(match.drops1, match.penalties1, match.tries1, match.conversions1)
        self.score_team2 = helpers.calculate_score(match.drops2, match.penalties2, match.tries2, match.conversions2)
        self.bonus_offensive_team1 = helpers.calculate_bonus_offensive(match.tries1, match.tries2)
        self.bonus_offensive_team2 = helpers.calculate_bonus_offensive(match.tries2, match.tries1)
        self.bonus_defensive_team1 = helpers.calculate_bonus_defensive(self.score_team1, self.score_team2)
        self.bonus_defensive_team2 = helpers.calculate_bonus_defensive(self.score_team2, self.score_team1)

    def __getattr__(self, key):
        if hasattr(self.match, key):
            return getattr(self.match, key)
        return getattr(self, key)

    def __setattr__(self, key, value):
        if hasattr(self.match, key):
            return setattr(self.match, key, value)
        return setattr(self, key, value)
