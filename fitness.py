import random


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

    # Pénalités pour chaque motif
    PENALTY_MATCH_REPEATED = 10
    PENALTY_MULTIPLE_MATCHES_PER_WEEK = 5
    PENALTY_EXCEED_PERIOD_LIMIT = 5
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
                    print(f"Semaine {week+1}, période {period+1}: Aucun match n'a été planifié. Pénalité ajoutée de {PENALTY_EMPTY_MATCH}")
                penalty_empty_match += 1
                continue

            team1, team2 = match

            # Pénalité si une équipe joue contre elle-même
            if team1 == team2:
                if verbose:
                    print(f"Semaine {week+1}, période {period+1}: L'équipe {team1} joue contre elle-même. Pénalité ajoutée de {PENALTY_SELF_MATCH}")
                penalty_self_match += 1

            # Pénalité si une équipe joue plus d'une fois dans la même semaine
            if team1 in teams_played_this_week:
                if verbose:
                    print(f"Semaine {week+1}, période {period+1}: L'équipe {team1} joue plus d'une fois cette semaine. Pénalité ajoutée de {PENALTY_MULTIPLE_MATCHES_PER_WEEK}")
                penalty_multiple_matches_per_week += 1
            if team2 in teams_played_this_week:
                if verbose:
                    print(f"Semaine {week+1}, période {period+1}: L'équipe {team2} joue plus d'une fois cette semaine. Pénalité ajoutée de {PENALTY_MULTIPLE_MATCHES_PER_WEEK}")
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
                    print(f"Semaine {week+1}, période {period+1}: Le match entre {team1} et {team2} a déjà eu lieu. Pénalité ajoutée de {PENALTY_MATCH_REPEATED}")
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
                    print(f"Période {period+1}: L'équipe {team} apparaît {period_appearances} fois dans cette période. Pénalité ajoutée de {PENALTY_EXCEED_PERIOD_LIMIT}")
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

    if verbose:
        print(f"Pénalité totale: {total_penalty} (Répétition de matchs: {penalty_repeated_matches}, "
                f"Matchs multiples par semaine: {penalty_multiple_matches_per_week}, "
                f"Limite de période dépassée: {penalty_exceed_period_limit}, "
                f"Matchs contre soi-même: {penalty_self_match}, "
                f"Matchs manquants: {penalty_missing_match}, "
                f"Périodes sans match: {penalty_empty_match})")

    return total_penalty

def find_match_in_exceed_period_limit(schedule):
    # Initialize the structure to track appearances and matches
    num_weeks = len(schedule)
    num_periods = len(schedule[0])
    appearances_per_period = {}
    matches_per_period = {}

    for week in range(num_weeks):
        for period in range(num_periods):
            match = schedule[week][period]
            if match:
                team1, team2 = match

                # Initialize appearances and matches for team1
                if team1 not in appearances_per_period:
                    appearances_per_period[team1] = [0] * num_periods
                    matches_per_period[team1] = [[] for _ in range(num_periods)]

                # Initialize appearances and matches for team2
                if team2 not in appearances_per_period:
                    appearances_per_period[team2] = [0] * num_periods
                    matches_per_period[team2] = [[] for _ in range(num_periods)]

                # Update appearances
                appearances_per_period[team1][period] += 1
                appearances_per_period[team2][period] += 1

                # Store the match for the current period
                matches_per_period[team1][period].append((week, period))
                matches_per_period[team2][period].append((week, period))

    # Check for teams exceeding the appearance limit
    for team, appearances in appearances_per_period.items():
        for period, period_appearances in enumerate(appearances):
            if period_appearances > 2:
                # Randomly select one of the matches that caused the exceedance
                match_list = matches_per_period[team][period]
                if match_list:
                    return random.choice(match_list)  # Return a random match (week, period)

    return None  # Return None if no team exceeds the appearance limit
