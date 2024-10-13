import random
import copy
import fitness

def local_search(schedule, num_teams, max_iterations=1000, verbose=False):
    current_schedule = schedule
    current_penalty = fitness.evaluate_schedule(current_schedule, num_teams, False)
    penalty_history = [(0, current_penalty)]

    for iteration in range(max_iterations):
        # Générer un voisin en échangeant deux matchs aléatoires
        new_schedule = copy.deepcopy(current_schedule)
        week1, period1 = random.randint(0, len(new_schedule) - 1), random.randint(0, len(new_schedule[0]) - 1)
        week2, period2 = random.randint(0, len(new_schedule) - 1), random.randint(0, len(new_schedule[0]) - 1)

        # si l'un des matchs est vide, on le remplace par un match aléatoire
        if new_schedule[week1][period1] is None:
            new_schedule[week1][period1] = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))
        if new_schedule[week2][period2] is None:
            new_schedule[week2][period2] = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))

        # Échanger les matchs
        new_schedule[week1][period1], new_schedule[week2][period2] = new_schedule[week2][period2], new_schedule[week1][period1]

        new_penalty = fitness.evaluate_schedule(new_schedule, num_teams, False)

        # Si le nouveau planning est meilleur, on l'adopte
        if new_penalty <= current_penalty:
            current_schedule = new_schedule
            current_penalty = new_penalty
            penalty_history.append((iteration, current_penalty))
            if verbose:
                print(f"Iteration {iteration}: Amélioration trouvée avec une pénalité de {new_penalty}")
                print(f"Changeant le match {week1 + 1}, {period1 + 1} avec le match {week2 + 1}, {period2 + 1}")
        else:
            # on essaie de changer une des équipes du match
            new_schedule = copy.deepcopy(current_schedule)
            if new_schedule[week1][period1] is None:
                new_schedule[week1][period1] = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))
                continue
                
            # Remplacez l'équipe à domicile pour le match
            original_team1 = new_schedule[week1][period1][0]
            new_team1 = random.randint(0, num_teams - 1)
            while new_team1 == original_team1:  # Éviter de choisir la même équipe
                new_team1 = random.randint(0, num_teams - 1)

            # Créer un nouveau match avec le nouveau tuple
            new_schedule[week1][period1] = (new_team1, new_schedule[week1][period1][1])  # Remplacer seulement l'équipe à domicile

            new_penalty = fitness.evaluate_schedule(new_schedule, num_teams, False)

            if new_penalty <= current_penalty:
                current_schedule = new_schedule
                current_penalty = new_penalty
                penalty_history.append((iteration, current_penalty))
                if verbose:
                    print(f"Iteration {iteration}: Amélioration trouvée avec une pénalité de {new_penalty}")
                    print(f"Changeant l'équipe à domicile pour le match {week1 + 1}, {period1 + 1}")

    if verbose:
        print(f"Recherche locale terminée après {max_iterations} itérations.")
        fitness.evaluate_schedule(current_schedule, num_teams, verbose)

    return current_schedule, current_penalty, penalty_history
