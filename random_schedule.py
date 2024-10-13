import random

def random_round_robin_schedule(num_teams):
    # Vérification que le nombre d'équipes est pair
    if num_teams % 2 != 0:
        raise ValueError("Le nombre d'équipes doit être pair.")

    # Initialisation
    num_weeks = num_teams - 1
    num_periods = num_teams // 2  # Nombre de matchs par semaine

    # Créer une liste des équipes
    teams = list(range(num_teams))

    # Matrice de planification : semaines x périodes (chaque cellule contiendra un match)
    schedule = [[None for _ in range(num_periods)] for _ in range(num_weeks)]

    # remplir aléatoirement la matrice de planification avec des matchs entre les équipes 0 et num_teams-1
    for week in range(num_weeks):
        for period in range(num_periods):
            home = random.choice(teams)
            away = random.choice(teams)
            schedule[week][period] = (home, away)

    return schedule
