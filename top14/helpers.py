from .models import Match


def calculate_points_direct(match, team1, team2):
    if match.score_team1 > match.score_team2:
        team1.nb_points_direct += 4
        team2.nb_points_direct += 0
    elif match.score_team1 < match.score_team2:
        team1.nb_points_direct += 0
        team2.nb_points_direct += 4
    else:
        team1.nb_points_direct += 2
        team2.nb_points_direct += 2

    if match.bonus_offensive_team1:
        team1.nb_points_direct += 1

    if match.bonus_defensive_team1:
        team1.nb_points_direct += 1

    if match.bonus_offensive_team2:
        team2.nb_points_direct += 1

    if match.bonus_defensive_team2:
        team2.nb_points_direct += 1

    if match.withdrawn_team1:
        team1.nb_points_direct -= 2

    if match.withdrawn_team2:
        team2.nb_points_direct -= 2


def calculate_diff_direct(match, team1, team2):
    team1.diff_direct += match.score_team1 - match.score_team2
    team2.diff_direct += match.score_team2 - match.score_team1


def calculate_tries_direct(match, team1, team2):
    team1.nb_tries_direct += match.tries1
    team2.nb_tries_direct += match.tries2


def get_match(matches, team1, team2):
    for m in matches:
        if m.team1 == team1 and m.team2 == team2:
            return m
    return None


def sort_ranking(ranking, matches):
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

    def direct_step(rank, next_step_needed, attr, invoke, matches):
        need_next_step = {}
        for index, need_rank in enumerate(next_step_needed):
            sublist = rank[need_rank['min']:need_rank['max'] + 1]
            for i in range(len(sublist) - 1):
                team1 = sublist[i]
                for j in range(len(sublist) - i - 1):
                    team2 = sublist[i + j + 1]
                    match = get_match(matches, team1, team2)
                    if match:
                        invoke(match, team1, team2)
                        invoke(match, team2, team1)
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
        return direct_step(rank, second_step_needed, 'nb_points_direct', calculate_points_direct, matches)

    def third_step(rank, third_step_needed):
        return simple_step(rank, third_step_needed, 'diff')

    def fourth_step(rank, fourth_step_needed):
        return direct_step(rank, fourth_step_needed, 'diff_direct', calculate_diff_direct, matches)

    def fifth_step(rank, fifth_step_needed):
        return direct_step(rank, fifth_step_needed, 'nb_tries_direct', calculate_tries_direct, matches)

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
