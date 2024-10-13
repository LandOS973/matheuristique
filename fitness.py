def evaluate_schedule(schedule, num_teams, verbose=True):
    num_weeks = len(schedule)
    num_periods = len(schedule[0])

    # Initialisation des pénalités
    penalty_repeated_matches = 0
    penalty_multiple_matches_per_week = 0
    penalty_exceed_period_limit = 0
    penalty_self_match = 0  # Pénalité pour les équipes jouant contre elles-mêmes
    penalty_missing_match = 0  # Pénalité pour les matchs non joués
    penalty_empty_match = 0  # Pénalité pour les périodes sans match
    penalty_match_against_self = 0  # Pénalité pour les matchs contre soi-même

    # Pénalités pour chaque motif
    PENALTY_MATCH_REPEATED = 10
    PENALTY_MULTIPLE_MATCHES_PER_WEEK = 5
    PENALTY_EXCEED_PERIOD_LIMIT = 2
    PENALTY_SELF_MATCH = 25
    PENALTY_MISSING_MATCH = 15
    PENALTY_EMPTY_MATCH = 25

    # Initialisation des structures de suivi
    match_counts = set()  # Utiliser un ensemble pour stocker les matchs joués
    appearances_per_period = {team: [0] * num_periods for team in range(num_teams)}  # Suivi des apparitions par période

    # Ensemble des paires d'équipes qui doivent se rencontrer exactement une fois
    required_matches = set((i, j) for i in range(num_teams) for j in range(i + 1, num_teams))

    # Parcourir la planification et calculer les pénalités
    for week in range(num_weeks):
        teams_played_this_week = set()

        for period in range(num_periods):
            match = schedule[week][period]
            if match is None:
                if verbose:
                    print(f"Semaine {week}, période {period}: Aucun match n'a été planifié. Pénalité ajoutée de {PENALTY_EMPTY_MATCH}")
                penalty_empty_match += 1
                continue

            team1, team2 = match

            # Pénalité si une équipe joue contre elle-même
            if team1 == team2:
                if verbose:
                    print(f"Semaine {week}, période {period}: L'équipe {team1} joue contre elle-même. Pénalité ajoutée de {PENALTY_SELF_MATCH}")
                penalty_self_match += 1

            # Pénalité si une équipe joue plus d'une fois dans la même semaine
            if team1 in teams_played_this_week:
                if verbose:
                    print(f"Semaine {week}, période {period}: L'équipe {team1} joue plus d'une fois cette semaine. Pénalité ajoutée de {PENALTY_MULTIPLE_MATCHES_PER_WEEK}")
                penalty_multiple_matches_per_week += 1
            if team2 in teams_played_this_week:
                if verbose:
                    print(f"Semaine {week}, période {period}: L'équipe {team2} joue plus d'une fois cette semaine. Pénalité ajoutée de {PENALTY_MULTIPLE_MATCHES_PER_WEEK}")
                penalty_multiple_matches_per_week += 1

            # Ajouter les équipes jouées cette semaine
            teams_played_this_week.add(team1)
            teams_played_this_week.add(team2)

            # Compter les apparitions des équipes dans cette période
            appearances_per_period[team1][period] += 1
            appearances_per_period[team2][period] += 1

            # Vérifier si le match a déjà été joué (sans ordre, grâce à l'ensemble)
            if frozenset([team1, team2]) in match_counts:
                if verbose:
                    print(f"Semaine {week+1}, période {period}: Le match entre {team1} et {team2} a déjà eu lieu. Pénalité ajoutée de {PENALTY_MATCH_REPEATED}")
                penalty_repeated_matches += 1
            else:
                match_counts.add(frozenset([team1, team2]))

            # Retirer le match joué de l'ensemble des matchs requis
            if (team1, team2) in required_matches:
                required_matches.remove((team1, team2))
            elif (team2, team1) in required_matches:
                required_matches.remove((team2, team1))
                
            

    # Pénalité pour les équipes jouant plus de deux fois dans une même période
    for team, appearances in appearances_per_period.items():
        for period, period_appearances in enumerate(appearances):
            if period_appearances > 2:
                if verbose:
                    print(f"Période {period}: L'équipe {team} apparaît {period_appearances} fois dans cette période. Pénalité ajoutée de {PENALTY_EXCEED_PERIOD_LIMIT}")
                penalty_exceed_period_limit += period_appearances - 2

    # Pénalité pour les matchs manquants (chaque paire non rencontrée)
    if required_matches:
        if verbose:
            print(f"Les paires d'équipes suivantes ne se sont jamais rencontrées:")
        for match in required_matches:
            if verbose:
                print(f"Équipe {match[0]} vs Équipe {match[1]}. Pénalité ajoutée de {PENALTY_MISSING_MATCH}")
        penalty_missing_match = len(required_matches) * PENALTY_MISSING_MATCH  # Pénalité importante pour les matchs manquants

    # Calcul du score total
    total_penalty = (
            penalty_repeated_matches * PENALTY_MATCH_REPEATED +
            penalty_multiple_matches_per_week * PENALTY_MULTIPLE_MATCHES_PER_WEEK +
            penalty_exceed_period_limit * PENALTY_EXCEED_PERIOD_LIMIT +
            penalty_self_match * PENALTY_SELF_MATCH +
            penalty_missing_match +
            penalty_empty_match * PENALTY_EMPTY_MATCH
            
    )

    return total_penalty
