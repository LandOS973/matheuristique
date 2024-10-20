import random
import copy
import math
import fitness

def simulated_annealing(schedule, num_teams, max_iterations=1000, initial_temp=100.0, cooling_rate=0.99, verbose=False):
    current_schedule = schedule
    current_penalty = fitness.evaluate_schedule(current_schedule, num_teams, False)
    penalty_history = [(0, current_penalty)]

    # Variables pour suivre la meilleure solution trouvée
    best_schedule = current_schedule
    best_penalty = current_penalty

    temperature = initial_temp  # Température initiale

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

        
        
        if random.random() < 0.5:
            # Échanger les matchs
            new_schedule[week1][period1], new_schedule[week2][period2] = new_schedule[week2][period2], new_schedule[week1][period1]
        else:
                new_schedule[week1][period1] = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))
                continue

        new_penalty = fitness.evaluate_schedule(new_schedule, num_teams, False)

        # Calcul de la variation de pénalité
        delta_penalty = new_penalty - current_penalty

        # Critère d'acceptation : meilleure solution ou selon une probabilité basée sur la température
        if delta_penalty < 0 or random.random() < math.exp(-delta_penalty / temperature):
            current_schedule = new_schedule
            current_penalty = new_penalty
            penalty_history.append((iteration, current_penalty))

            # Mise à jour de la meilleure solution trouvée
            if current_penalty < best_penalty:
                best_schedule = current_schedule
                best_penalty = current_penalty

            if verbose:
                print(f"Iteration {iteration}: Solution acceptée avec une pénalité de {new_penalty}")
                print(f"Changeant le match {week1 + 1}, {period1 + 1} avec le match {week2 + 1}, {period2 + 1}")

        # Refroidissement : on diminue la température
        temperature *= cooling_rate

        # Arrêter si la température devient trop basse
        if temperature < 1e-3:
            break

    if verbose:
        print(f"Recuit simulé terminé après {iteration + 1} itérations.")
        print(f"Meilleure pénalité trouvée : {best_penalty}")
        fitness.evaluate_schedule(best_schedule, num_teams, verbose)

    return best_schedule, best_penalty, penalty_history
