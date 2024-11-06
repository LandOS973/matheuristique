import random
import copy
import math
import fitness
import local_search_descente
import random_schedule


def simulated_annealing(schedule, num_teams, max_iterations=1000, initial_temp=100.0, cooling_rate=0.99, verbose=False):
    current_schedule = schedule
    current_penalty = fitness.evaluate_schedule(current_schedule, num_teams, False)
    penalty_history = [(0, current_penalty)]

    # Variables pour suivre la meilleure solution trouvée
    best_schedule = current_schedule
    best_penalty = current_penalty

    temperature = initial_temp  # Température initiale
    stuck = 0

    for iteration in range(max_iterations):
        if current_penalty == 0 or stuck > 100:
            break
        # Générer un voisin en échangeant deux matchs aléatoires
        new_schedule = copy.deepcopy(current_schedule)
        week1, period1 = random.randint(0, len(new_schedule) - 1), random.randint(0, len(new_schedule[0]) - 1)
        week2, period2 = random.randint(0, len(new_schedule) - 1), random.randint(0, len(new_schedule[0]) - 1)

        # si l'un des matchs est vide, on le remplace par un match aléatoire
        if new_schedule[week1][period1] is None:
            new_schedule[week1][period1] = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))
        if new_schedule[week2][period2] is None:
            new_schedule[week2][period2] = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))



        if random.random() < 0.9:
            # Échanger les matchs
            new_schedule[week1][period1], new_schedule[week2][period2] = new_schedule[week2][period2], new_schedule[week1][period1]
        else:
                new_schedule[week1][period1] = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))
                continue

        new_penalty = fitness.evaluate_schedule(new_schedule, num_teams, False)

        # Calcul de la variation de pénalité
        delta_penalty = new_penalty - current_penalty
        stuck += 1
        # Critère d'acceptation : meilleure solution ou selon une probabilité basée sur la température
        if delta_penalty < 0 or random.random() < math.exp(-delta_penalty / temperature):
            current_schedule, current_penalty,_ = local_search_descente.local_search(new_schedule, num_teams, max_iterations=5000, verbose=False)
            stuck = 0
            # Mise à jour de la meilleure solution trouvée
            if current_penalty < best_penalty:
                best_schedule = current_schedule
                best_penalty = current_penalty

            if verbose:
                print(f"Iteration {iteration}: Solution acceptée avec une pénalité de {new_penalty}")
                print(f"Changeant le match {week1 + 1}, {period1 + 1} avec le match {week2 + 1}, {period2 + 1}")
            penalty_history.append((iteration, current_penalty))

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

def test_simulated_annealing_with_differente_temperature():
    num_teams = 12
    temperature = range(50, 200, 5)
    scores = []
    for temp in temperature:
        schedule = random_schedule.random_round_robin_schedule(num_teams)

        _, penalty, _ = simulated_annealing(schedule, num_teams, initial_temp=temp, verbose=False)
        scores.append([temp, penalty])
        print(f"Température : {temp}, Pénalité : {penalty}")
    return scores
import numpy as np
def test_simulated_annealing_with_differente_cooling_rate():
    num_teams = 12
    cooling_rates = np.arange(0.8, 1, 0.01)
    scores = []
    for rate in cooling_rates:
        schedule = random_schedule.random_round_robin_schedule(num_teams)

        _, penalty, _ = simulated_annealing(schedule, num_teams, cooling_rate=rate, verbose=False)
        scores.append([rate, penalty])
        print(f"Taux de refroidissement : {rate}, Pénalité : {penalty}")
    return scores

import matplotlib.pyplot as plt
if __name__ == '__main__':
    num_teams = 12
    results = test_simulated_annealing_with_differente_cooling_rate()

    # Séparer les tailles de populations et les pénalités
    rate, penalty = zip(*results)

    # Trouver l'indice du score de fitness le plus faible
    min_index = penalty.index(min(penalty))
    min_temp = rate[min_index]
    min_penalty = penalty[min_index]

    # Tracer la courbe des pénalités en fonction des tailles de population
    plt.plot(rate, penalty, label='Score de fitness')
    plt.xlabel('Cooling rate')
    plt.ylabel('Score fitness')
    plt.title('Recuit : Influence du refroidissement (12 équipes)')

    # Ajouter une croix rouge au point avec le score de fitness le plus faible
    plt.plot(min_temp, min_penalty, 'rX', markersize=10, label='Score minimum')

    # Ajouter une légende pour identifier la croix rouge
    plt.legend()

    # Afficher le graphique
    plt.show()