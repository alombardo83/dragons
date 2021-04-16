from django.contrib.auth.models import DoesNotExist

from .models import Match


def calculate_score(drops, penalties, tries, conversions):
    return 3 * drops + 3 * penalties + 5 * tries + 2 * conversions


def calculate_bonus_offensive(tries1, tries2):
    return tries1 >= tries2 + 3


def calculate_bonus_defensive(score1, score2):
    return score1 < score2 <= score1 + 5


def calculate_points_direct(team1, team2):
    try:
        match = Match.objects.filter(season__active=True, played=True, team1__id=team1.id,
                                     team2__id=team2.id).get()
    except DoesNotExist:
        return

    score_team1 = calculate_score(match.drops1, match.penalties1, match.tries1,
                                  match.conversions1)
    score_team2 = calculate_score(match.drops2, match.penalties2, match.tries2,
                                  match.conversions2)

    if score_team1 > score_team2:
        team1.nb_points_direct += 4
        team2.nb_points_direct += 0
    elif score_team1 < score_team2:
        team1.nb_points_direct += 0
        team2.nb_points_direct += 4
    else:
        team1.nb_points_direct += 2
        team2.nb_points_direct += 2

    if calculate_bonus_offensive(match.tries1, match.tries2):
        team1.nb_points_direct += 1

    if calculate_bonus_defensive(score_team1, score_team2):
        team1.nb_points_direct += 1

    if calculate_bonus_offensive(match.tries2, match.tries1):
        team2.nb_points_direct += 1

    if calculate_bonus_defensive(score_team2, score_team1):
        team2.nb_points_direct += 1

    if match.withdrawn_team1:
        team1.nb_points_direct -= 2

    if match.withdrawn_team2:
        team2.nb_points_direct -= 2


def calculate_diff_direct(team1, team2):
    try:
        match = Match.objects.filter(season__active=True, played=True, team1__id=team1.id,
                                     team2__id=team2.id).get()
    except DoesNotExist:
        return

    score_team1 = calculate_score(match.drops1, match.penalties1, match.tries1,
                                  match.conversions1)
    score_team2 = calculate_score(match.drops2, match.penalties2, match.tries2,
                                  match.conversions2)

    team1.diff_direct += score_team1 - score_team2
    team2.diff_direct += score_team2 - score_team1


def calculate_tries_direct(team1, team2):
    try:
        match = Match.objects.filter(season__active=True, played=True, team1__id=team1.id,
                                     team2__id=team2.id).get()
    except DoesNotExist:
        return

    team1.nb_tries_direct += match.tries1
    team2.nb_tries_direct += match.tries2


def sort_ranking(ranking):
    def simple_step(rank, next_step_needed, attr, reverse=True):
        need_next_step = {}
        for index, need_rank in enumerate(next_step_needed):
            sublist = rank[need_rank['min']:need_rank['max'] + 1]
            sublist = sorted(sublist, key=lambda t: getattr(t, attr), reverse=reverse)
            rank[need_rank['min']:need_rank['max'] + 1] = sublist
            for i, team in enumerate(sublist):
                key = str(index) + ':' + str(getattr(team, attr))
                if key not in need_next_step:
                    need_next_step[key] = {'min': need_rank['min'] + i, 'max': need_rank['min'] + i}
                need_next_step[key]['max'] = need_rank['min'] + i
        return rank, [v for v in need_next_step.values() if v['min'] != v['max']]

    def direct_step(rank, next_step_needed, attr, invoke):
        need_next_step = {}
        for index, need_rank in enumerate(next_step_needed):
            sublist = rank[need_rank['min']:need_rank['max'] + 1]
            for i in range(len(sublist) - 1):
                team1 = sublist[i]
                for j in range(len(sublist) - i - 1):
                    team2 = sublist[i + j + 1]
                    invoke(team1, team2)
                    invoke(team2, team1)
            sublist = sorted(sublist, key=lambda t: getattr(t, attr), reverse=True)
            rank[need_rank['min']:need_rank['max'] + 1] = sublist
            for i, team in enumerate(sublist):
                key = str(index) + ':' + str(getattr(team, attr))
                if key not in need_next_step:
                    need_next_step[key] = {'min': need_rank['min'] + i, 'max': need_rank['min'] + i}
                need_next_step[key]['max'] = need_rank['min'] + i
        return rank, [v for v in need_next_step.values() if v['min'] != v['max']]

    def first_step(rank):
        return simple_step(rank, [{'min': 0, 'max': 14}], 'nb_points')

    def second_step(rank, second_step_needed):
        return direct_step(rank, second_step_needed, 'nb_points_direct', calculate_points_direct)

    def third_step(rank, third_step_needed):
        return simple_step(rank, third_step_needed, 'diff')

    def fourth_step(rank, fourth_step_needed):
        return direct_step(rank, fourth_step_needed, 'diff_direct', calculate_diff_direct)

    def fifth_step(rank, fifth_step_needed):
        return direct_step(rank, fifth_step_needed, 'nb_tries_direct', calculate_tries_direct)

    def sixth_step(rank, sixth_step_needed):
        return simple_step(rank, sixth_step_needed, 'diff_tries')

    def seventh_step(rank, seventh_step_needed):
        return simple_step(rank, seventh_step_needed, 'nb_total_score')

    def eighth_step(rank, eighth_step_needed):
        return simple_step(rank, eighth_step_needed, 'nb_tries_marked')

    def ninth_step(rank, ninth_step_needed):
        return simple_step(rank, ninth_step_needed, 'nb_withdrawn', reverse=False)

    def tenth_step(rank, tenth_step_needed):
        return simple_step(rank, tenth_step_needed, 'last_ranking', reverse=False)

    res, need_next_step = first_step(ranking)
    res, need_next_step = second_step(res, need_next_step)
    res, need_next_step = third_step(res, need_next_step)
    res, need_next_step = fourth_step(res, need_next_step)
    res, need_next_step = fifth_step(res, need_next_step)
    res, need_next_step = sixth_step(res, need_next_step)
    res, need_next_step = seventh_step(res, need_next_step)
    res, need_next_step = eighth_step(res, need_next_step)
    res, need_next_step = ninth_step(res, need_next_step)
    res, need_next_step = tenth_step(res, need_next_step)
    return res
