import fitness


def round_robin_schedule(num_teams):
    # Vérification que le nombre d'équipes est pair
    if num_teams % 2 != 0:
        raise ValueError("Le nombre d'équipes doit être pair.")

    # Initialisation
    num_weeks = num_teams - 1  # Chaque équipe joue contre toutes les autres
    num_periods = num_teams // 2  # Nombre de périodes par semaine

    # Créer une liste des équipes
    teams = list(range(num_teams))

    # Matrice de planification : semaines x périodes (chaque cellule contiendra un match)
    schedule = [[None for _ in range(num_periods)] for _ in range(num_weeks)]

    # Dictionnaire pour suivre le nombre d'apparitions de chaque équipe dans chaque période
    appearances_per_period = {team: [0] * num_periods for team in teams}

    # Générer les matchs en mode glouton
    for week in range(num_weeks):
        matches_for_week = set()  # Pour suivre les équipes déjà programmées cette semaine
        period_idx = 0

        for i in range(num_periods):
            team1 = teams[i]
            team2 = teams[num_teams - i - 1]

            # Vérifie si les équipes peuvent être ajoutées sans conflit et sans dépasser la limite d'apparitions
            if (team1 not in matches_for_week and team2 not in matches_for_week
                    and appearances_per_period[team1][period_idx] < 2
                    and appearances_per_period[team2][period_idx] < 2):
                # Ajouter le match s'il n'y a pas de conflit et les équipes n'ont pas dépassé leur limite
                schedule[week][period_idx] = (team1, team2)
                matches_for_week.add(team1)
                matches_for_week.add(team2)

                # Mettre à jour le nombre d'apparitions des équipes dans la période
                appearances_per_period[team1][period_idx] += 1
                appearances_per_period[team2][period_idx] += 1

                period_idx += 1

        # Rotation des équipes (sauf le premier élément)
        teams = [teams[0]] + teams[-1:] + teams[1:-1]

    return schedule


if __name__ == "__main__":
    num_teams = 8
    best_schedule = round_robin_schedule(num_teams)
    print("\nÉvaluation du schedule:")
    print(fitness.evaluate_schedule(best_schedule, num_teams, verbose=True))
    print("\nPlanification des matchs (avec périodes):")
    print(best_schedule)
