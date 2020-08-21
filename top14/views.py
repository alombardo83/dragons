from django.shortcuts import render
from datetime import datetime
from functools import total_ordering
from .models import Season, Match, Team, ROUNDS

def _calculate_score(drops, penalties, tries, conversions):
    return 3 * drops + 3 * penalties + 5 * tries + 2 * conversions

def _calculate_bonus_offensive(tries1, tries2):
    return tries1 >= tries2 + 3

def _calculate_bonus_defensive(score1, score2):
    return score1 < score2 and score1 + 5 >= score2

def index(request):
    template_name = 'top14/index.html'
    season = Season.objects.filter(active=True).get()
    
    ranking = []
    teams = Team.objects.filter(active=True).all()
    for t in teams:
        ranking.append(TeamDisplay(t))
    
    display_matches = []
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
                team1 = list(filter(lambda t: (t.id == match.team1.id), ranking))[0]
                team2 = list(filter(lambda t: (t.id == match.team2.id), ranking))[0]
                team1._compute_match_results(m.score_team1, m.score_team2, m.bonus_offensive_team1, m.bonus_defensive_team1, m.withdrawn_team1, match.tries1, match.tries2)
                team2._compute_match_results(m.score_team2, m.score_team1, m.bonus_offensive_team2, m.bonus_defensive_team2, m.withdrawn_team2, match.tries2, match.tries1)
        
        display_matches.append(round_matches)

    ranking.sort()
    return render(request, template_name, {'matches': display_matches, 'ranking': ranking})

@total_ordering
class TeamDisplay():
    id = 0
    name = ''
    last_ranking = 0
    nb_points = 0
    nb_played = 0
    nb_won = 0
    nb_draw = 0
    nb_lost = 0
    nb_bonus_offensive = 0
    nb_bonus_defensive = 0
    nb_withdrawn = 0
    diff = 0
    nb_tries_marked = 0
    nb_tries_conceded = 0
    nb_total_score = 0
    
    def __init__(self, team):
        self.id = team.id
        self.name = team.name
        self.nb_points -= team.penalty_points
        self.last_ranking = team.last_ranking
    
    def __eq__(self, other):
        return (self.id == other.id)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        season = Season.objects.filter(active=True).get()
        
        nb_points_team1 = 0
        nb_points_team2 = 0
        diff_team1 = 0
        diff_team2 = 0
        nb_tries1 = 0
        nb_tries2 = 0
        
        try:
            match = Match.objects.filter(season__id=season.id, played=True, team1__id=self.id, team2__id=other.id).get()
            score_team1 = _calculate_score(match.drops1, match.penalties1, match.tries1, match.conversions1)
            score_team2 = _calculate_score(match.drops2, match.penalties2, match.tries2, match.conversions2)
            
            diff_team1 += (score_team1 - score_team2)
            diff_team2 += (score_team2 - score_team1)
            nb_tries1 += match.tries1
            nb_tries2 += match.tries2
            
            if score_team1 > score_team2:
                nb_points_team1 += 4
                nb_points_team2 += 0
            elif score_team1 < score_team2:
                nb_points_team1 += 0
                nb_points_team2 += 4
            else:
                nb_points_team1 += 2
                nb_points_team2 += 2
            
            if _calculate_bonus_offensive(match.tries1, match.tries2):
                nb_points_team1 += 1
            
            if _calculate_bonus_defensive(score_team1, score_team2):
                nb_points_team1 += 1
            
            if _calculate_bonus_offensive(match.tries2, match.tries1):
                nb_points_team2 += 1
            
            if _calculate_bonus_defensive(score_team2, score_team1):
                nb_points_team2 += 1
            
            if match.withdrawn_team1:
                nb_points_team1 -= 2
            
            if match.withdrawn_team2:
                nb_points_team2 -= 2
        except:
            pass
        
        try:
            match = Match.objects.filter(season__id=season.id, played=True, team2__id=self.id, team1__id=other.id).get()
            score_team1 = _calculate_score(match.drops1, match.penalties1, match.tries1, match.conversions1)
            score_team2 = _calculate_score(match.drops2, match.penalties2, match.tries2, match.conversions2)
            
            diff_team1 += (score_team1 - score_team2)
            diff_team2 += (score_team2 - score_team1)
            nb_tries1 += match.tries1
            nb_tries2 += match.tries2
            
            if score_team1 > score_team2:
                nb_points_team1 += 4
                nb_points_team2 += 0
            elif score_team1 < score_team2:
                nb_points_team1 += 0
                nb_points_team2 += 4
            else:
                nb_points_team1 += 2
                nb_points_team2 += 2
            
            if _calculate_bonus_offensive(match.tries1, match.tries2):
                nb_points_team1 += 1
            
            if _calculate_bonus_defensive(score_team1, score_team2):
                nb_points_team1 += 1
            
            if _calculate_bonus_offensive(match.tries2, match.tries1):
                nb_points_team2 += 1
            
            if _calculate_bonus_defensive(score_team2, score_team1):
                nb_points_team2 += 1
            
            if match.withdrawn_team1:
                nb_points_team1 -= 2
            
            if match.withdrawn_team2:
                nb_points_team2 -= 2
        except:
            pass
        
        if self.nb_points != other.nb_points:
            return self.nb_points > other.nb_points
        
        print('{} {} - {} {}'.format(self.id, nb_points_team1, other.id, nb_points_team2))
        if nb_points_team1 != nb_points_team2:
            return nb_points_team1 > nb_points_team2
        
        if self.diff != other.diff:
            return self.diff > other.diff
        
        if diff_team1 != diff_team2:
            return diff_team1 > diff_team2
        
        if nb_tries1 != nb_tries2:
            return nb_tries1 > nb_tries2
        
        diff_tries1 = self.nb_tries_marked - self.nb_tries_conceded
        diff_tries2 = other.nb_tries_marked - other.nb_tries_conceded
        if diff_tries1 != diff_tries2:
            return diff_tries1 > diff_tries2
        
        if self.nb_total_score != other.nb_total_score:
            return self.nb_total_score > other.nb_total_score
        
        if self.nb_tries_marked != other.nb_tries_marked:
            return self.nb_tries_marked > other.nb_tries_marked
        
        if self.nb_withdrawn != other.nb_withdrawn:
            return self.nb_withdrawn < other.nb_withdrawn
        
        return self.last_ranking < other.last_ranking
    
    def _compute_match_results(self, score1, score2, bonus_offensive, bonus_defensive, withdrawn, tries1, tries2):
        self.nb_played += 1
        self.diff += (score1 - score2)
        self.nb_tries_marked += tries1
        self.nb_tries_conceded += tries2
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

class MatchDisplay():
    date_time = datetime.today()
    played = False
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
    withdrawn_team1 = False
    withdrawn_team2 = False
    
    def __init__(self, match):
        self.date_time = match.date_time
        self.played = match.played
        self.name_team1 = match.team1.name
        self.name_team2 = match.team2.name
        self.short_name_team1 = match.team1.short_name
        self.short_name_team2 = match.team2.short_name
        self.score_team1 = _calculate_score(match.drops1, match.penalties1, match.tries1, match.conversions1)
        self.score_team2 = _calculate_score(match.drops2, match.penalties2, match.tries2, match.conversions2)
        self.bonus_offensive_team1 = _calculate_bonus_offensive(match.tries1, match.tries2)
        self.bonus_offensive_team2 = _calculate_bonus_offensive(match.tries2, match.tries1)
        self.bonus_defensive_team1 = _calculate_bonus_defensive(self.score_team1, self.score_team2)
        self.bonus_defensive_team2 = _calculate_bonus_defensive(self.score_team2, self.score_team1)
        self.withdrawn_team1 = match.withdrawn_team1
        self.withdrawn_team2 = match.withdrawn_team2
