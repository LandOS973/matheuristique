import random

def round_robin_schedule(num_teams):
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

    # Initialisation du compteur pour suivre les apparitions des équipes par période
    appearances_per_period = {team: [0] * num_periods for team in teams}

    # Algorithme glouton pour créer la planification
    for week in range(num_weeks):
        # Faire tourner les équipes à chaque semaine
        # La première équipe reste fixe, les autres tournent
        round_teams = [teams[0]] + teams[week+1:] + teams[1:week+1]

        # Périodes non encore remplies pour la semaine en cours
        period_filled = [False] * num_periods

        # Mélanger les équipes pour introduire un peu d'aléatoire
        random.shuffle(round_teams)

        for i in range(len(round_teams) // 2):
            home = round_teams[i]
            away = round_teams[-1-i]

            # Essayer de trouver une période disponible où les deux équipes peuvent jouer
            assigned = False
            for period in range(num_periods):
                if appearances_per_period[home][period] < 2 and appearances_per_period[away][period] < 2 and not period_filled[period]:
                    # Assigner le match dans la période correspondante
                    schedule[week][period] = (home, away)

                    # Mettre à jour le compteur d'apparitions pour chaque équipe dans cette période
                    appearances_per_period[home][period] += 1
                    appearances_per_period[away][period] += 1
                    period_filled[period] = True  # Marquer cette période comme remplie pour cette semaine
                    assigned = True
                    break

            # Si aucun créneau n'a été trouvé, assigner dans une période non remplie
            if not assigned:
                for period in range(num_periods):
                    if not period_filled[period]:
                        schedule[week][period] = (home, away)
                        period_filled[period] = True
                        break

    return schedule

# Fonction d'affichage pour la planification
def print_schedule(schedule):
    for week, matches in enumerate(schedule):
        print(f"Semaine {week+1}:")
        for period, match in enumerate(matches):
            if match:
                print(f"  Période {period}: Équipe {match[0]} vs Équipe {match[1]}")
            else:
                print(f"  Période {period}: (vide)")
        print()

# Exemple d'utilisation pour 8 équipes
num_teams = 8
schedule = round_robin_schedule(num_teams)
print_schedule(schedule)
