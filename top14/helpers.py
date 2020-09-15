def calculate_score(drops, penalties, tries, conversions):
    return 3 * drops + 3 * penalties + 5 * tries + 2 * conversions

def calculate_bonus_offensive(tries1, tries2):
    return tries1 >= tries2 + 3

def calculate_bonus_defensive(score1, score2):
    return score1 < score2 and score1 + 5 >= score2
