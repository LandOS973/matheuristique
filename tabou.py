import random
import copy
import fitness
import glouton
import numpy as np
import matplotlib.pyplot as plt

import random_schedule


def print_schedule(schedule, filename='schedule.png'):
    num_weeks = len(schedule)
    num_periods = len(schedule[0]) if num_weeks > 0 else 0

    # Créer une matrice pour représenter le tableau
    schedule_matrix = np.full((num_weeks, num_periods), '', dtype=object)

    # Remplir la matrice avec les équipes ou une indication de cellule vide
    for week in range(num_weeks):
        for period in range(num_periods):
            match = schedule[week][period]
            if match:
                schedule_matrix[week, period] = f"{match[0]} vs {match[1]}"
            else:
                schedule_matrix[week, period] = "(vide)"

    # Créer une figure et des axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Afficher le tableau avec Matplotlib
    ax.axis('tight')
    ax.axis('off')

    # Créer un tableau à partir de la matrice
    table = ax.table(cellText=schedule_matrix,
                     colLabels=[f"Période {i+1}" for i in range(num_periods)],
                     rowLabels=[f"Semaine {i+1}" for i in range(num_weeks)],
                     cellLoc='center',
                     loc='center')

    # Personnaliser l'apparence du tableau
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)  # Ajustez la taille des cellules si nécessaire

    # Sauvegarder l'image du tableau
    plt.savefig(filename, bbox_inches='tight')
    plt.show()  # Afficher le tableau


def tabou_search(schedule, num_teams, max_iterations=1000, tabu_tenure=50, verbose=False):
    current_schedule = schedule
    current_penalty = fitness.evaluate_schedule(current_schedule, num_teams, False)
    penalty_history = [(0, current_penalty)]

    best_schedule = copy.deepcopy(current_schedule)
    best_penalty = current_penalty

    tabu_list = []  # Liste des mouvements tabous

    for iteration in range(max_iterations):
        if current_penalty == 0:
            break
        move = None
        # Générer un voisin en fonction de la probabilité
        new_schedule = copy.deepcopy(current_schedule)
        if random.random() < 0.1:  # Avec une probabilité de 10 %, faire un changement aléatoire
            week, period = random.randint(0, len(new_schedule) - 1), random.randint(0, len(new_schedule[0]) - 1)
            # Générer un match aléatoire
            new_match = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))
            move = ("random_change", week, period, new_schedule[week][period])

            if move in tabu_list:
                continue

            # Appliquer le changement aléatoire
            new_schedule[week][period] = new_match
        else:  # Sinon, faire un échange de deux matchs
            week1, period1 = random.randint(0, len(new_schedule) - 1), random.randint(0, len(new_schedule[0]) - 1)
            week2, period2 = random.randint(0, len(new_schedule) - 1), random.randint(0, len(new_schedule[0]) - 1)

            # Vérifier que l'échange ne figure pas dans la liste taboue
            move = ((week1, period1), (week2, period2))
            if move in tabu_list:
                continue

            # Appliquer l'échange
            new_schedule[week1][period1], new_schedule[week2][period2] = new_schedule[week2][period2], new_schedule[week1][period1]

        # Calculer la pénalité de la nouvelle solution
        new_penalty = fitness.evaluate_schedule(new_schedule, num_teams, False)

        # Critère d'acceptation
        if new_penalty < current_penalty:
            tabu_list.append(move)
            current_schedule = new_schedule
            current_penalty = new_penalty

            # Mettre à jour la meilleure solution trouvée
            if new_penalty < best_penalty:
                best_schedule = new_schedule
                best_penalty = new_penalty
                if verbose:
                    print(f"Iteration {iteration}: Nouvelle meilleure solution avec une pénalité de {new_penalty}")

            # Ajouter le mouvement dans la liste taboue
            tabu_list.append(move)
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)  # Supprimer le mouvement le plus ancien si la liste dépasse la taille
        penalty_history.append((iteration, current_penalty))
        if verbose:
            print(f"Iteration {iteration}: Pénalité actuelle {current_penalty}")

    if verbose:
        print(f"Recherche tabou terminée après {max_iterations} itérations.")
        fitness.evaluate_schedule(best_schedule, num_teams, verbose)
    print(tabu_list)
    return best_schedule, best_penalty, penalty_history


if __name__ == "__main__":
    num_teams = 12
    schedule = random_schedule.random_round_robin_schedule(num_teams)
    best_schedule, penalty, penalty_history = tabou_search(schedule, num_teams, max_iterations=30000, verbose=True)
    print(f"Score de la planification (pénalités totales): {penalty}")
    print_schedule(best_schedule)
    print(best_schedule)

    # Pour tracer les pénalités
    iterations = [entry[0] for entry in penalty_history]
    penalties = [entry[1] for entry in penalty_history]

    plt.plot(iterations, penalties)
    plt.xlabel('Itérations')
    plt.ylabel('Pénalités')
    plt.title('Évolution des pénalités de la recherche tabou')
    plt.show()
