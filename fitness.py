def evaluate_schedule(schedule, num_teams):
    num_weeks = len(schedule)
    num_periods = len(schedule[0])

    # Initialisation des pénalités
    penalty_repeated_matches = 0
    penalty_multiple_matches_per_week = 0
    penalty_exceed_period_limit = 0
    penalty_self_match = 0  # Pénalité pour les équipes jouant contre elles-mêmes
    penalty_missing_match = 0  # Pénalité pour les matchs non joués


    # Pénalités pour chaque motif
    PENALITY_MATCH_REPEATED = 10
    PENALITY_MULTIPLE_MATCHES_PER_WEEK = 5
    PENALITY_EXCEED_PERIOD_LIMIT = 2
    PENALITY_SELF_MATCH = 20
    PENALITY_MISSING_MATCH = 15

    # Initialisation des structures de suivi
    match_counts = {}  # Suivi des matchs joués
    appearances_per_period = {team: [0] * num_periods for team in range(num_teams)}  # Suivi des apparitions par période

    # Ensemble des paires d'équipes qui doivent se rencontrer exactement une fois
    required_matches = set((i, j) for i in range(num_teams) for j in range(i + 1, num_teams))

    # Parcourir la planification et calculer les pénalités
    for week in range(num_weeks):
        teams_played_this_week = set()

        for period in range(num_periods):
            match = schedule[week][period]
            if match is None:
                continue  # Si la période est vide, on passe

            team1, team2 = match

            # Pénalité si une équipe joue contre elle-même
            if team1 == team2:
                print(f"Semaine {week}, période {period}: L'équipe {team1} joue contre elle-même. Pénalité ajoutée de " + str(PENALITY_SELF_MATCH))
                penalty_self_match += 1

            # Pénalité si une équipe joue plus d'une fois dans la même semaine
            if team1 in teams_played_this_week:
                print(f"Semaine {week}, période {period}: L'équipe {team1} joue plus d'une fois cette semaine. Pénalité ajoutée de " + str(PENALITY_MULTIPLE_MATCHES_PER_WEEK))
                penalty_multiple_matches_per_week += 1
            if team2 in teams_played_this_week:
                print(f"Semaine {week}, période {period}: L'équipe {team2} joue plus d'une fois cette semaine. Pénalité ajoutée de " + str(PENALITY_MULTIPLE_MATCHES_PER_WEEK))
                penalty_multiple_matches_per_week += 1

            # Ajouter les équipes jouées cette semaine
            teams_played_this_week.add(team1)
            teams_played_this_week.add(team2)

            # Compter les apparitions des équipes dans cette période
            appearances_per_period[team1][period] += 1
            appearances_per_period[team2][period] += 1

            # Vérifier si le match a déjà été joué
            if (team1, team2) in match_counts or (team2, team1) in match_counts:
                print(f"Semaine {week}, période {period}: Le match entre {team1} et {team2} a déjà eu lieu. Pénalité ajoutée de " + str(PENALITY_MATCH_REPEATED))
                penalty_repeated_matches += 1
            else:
                match_counts[(team1, team2)] = 1

            # Retirer le match joué de l'ensemble des matchs requis
            if (team1, team2) in required_matches:
                required_matches.remove((team1, team2))
            elif (team2, team1) in required_matches:
                required_matches.remove((team2, team1))

    # Pénalité pour les équipes jouant plus de deux fois dans une même période
    for team, appearances in appearances_per_period.items():
        for period, period_appearances in enumerate(appearances):
            if period_appearances > 2:
                print(f"Période {period}: L'équipe {team} apparaît {period_appearances} fois dans cette période. Pénalité ajoutée de " + str(PENALITY_EXCEED_PERIOD_LIMIT))
                penalty_exceed_period_limit += period_appearances - 2

    # Pénalité pour les matchs manquants (chaque paire non rencontrée)
    if required_matches:
        print(f"Les paires d'équipes suivantes ne se sont jamais rencontrées:")
        for match in required_matches:
            print(f"Équipe {match[0]} vs Équipe {match[1]}. Pénalité ajoutée de " + str(PENALITY_MISSING_MATCH))
        penalty_missing_match = len(required_matches) * PENALITY_MISSING_MATCH  # Pénalité importante pour les matchs manquants

    # Calcule du score total
    total_penalty = (
        penalty_repeated_matches * PENALITY_MATCH_REPEATED +
        penalty_multiple_matches_per_week * PENALITY_MULTIPLE_MATCHES_PER_WEEK +
        penalty_exceed_period_limit * PENALITY_EXCEED_PERIOD_LIMIT +
        penalty_self_match * PENALITY_SELF_MATCH +
        penalty_missing_match
    )

    return total_penalty

# Exemple d'utilisation pour tester les pénalités et motifs
schedule = [
    [(0, 1), (2, 3), (4, 5), (6, 7)],
    [(0, 0), (1, 7), (3, 5), (4, 6)],
    [(4, 7), (0, 3), (1, 6), (2, 5)],
    [(3, 6), (5, 7), (0, 4), (1, 2)],
    [(3, 7), (1, 4), (2, 6), (0, 5)],
    [(1, 5), (0, 6), (2, 7), (3, 4)],
    [(2, 4), (5, 6), (0, 7), (1, 3)]
]

num_teams = 8
penalty = evaluate_schedule(schedule, num_teams)
print("\n")
print(f"Score de la planification (pénalités totales): {penalty}")
