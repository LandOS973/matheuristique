import random
import copy
import fitness
import glouton
import random_schedule
import numpy as np
import matplotlib.pyplot as plt

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


def local_search(schedule, num_teams, max_iterations=1000, verbose=False):
    current_schedule = schedule
    current_penalty = fitness.evaluate_schedule(current_schedule, num_teams, False)
    penalty_history = [(0, current_penalty)]

    for iteration in range(max_iterations):
        if current_penalty == 0:
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
            new_schedule[week1][period1], new_schedule[week2][period2] = new_schedule[week2][period2], \
            new_schedule[week1][period1]
        else:
            new_schedule[week1][period1] = (random.randint(0, num_teams - 1), random.randint(0, num_teams - 1))



        new_penalty = fitness.evaluate_schedule(new_schedule, num_teams, False)

        # Si le nouveau planning est meilleur, on l'adopte
        if new_penalty < current_penalty:
            current_schedule = new_schedule
            current_penalty = new_penalty
            penalty_history.append((iteration, current_penalty))
            if verbose:
                print(f"Iteration {iteration}: Amélioration trouvée avec une pénalité de {new_penalty}")
        penalty_history.append((iteration, current_penalty))

    if verbose:
        print(f"Recherche locale terminée après {max_iterations} itérations.")
        fitness.evaluate_schedule(current_schedule, num_teams, verbose)

    return current_schedule, current_penalty, penalty_history


if __name__ == "__main__":
    num_teams = 12
    schedule = glouton.round_robin_schedule(num_teams)
    schedule, penalty, penalty_history = local_search(schedule, num_teams, max_iterations=100000, verbose=True)
    print(f"Score de la planification (pénalités totales): {penalty}")
    print_schedule(schedule)
    print(schedule)

    # Pour tracer les pénalités
    import matplotlib.pyplot as plt

    iterations = [entry[0] for entry in penalty_history]
    penalties = [entry[1] for entry in penalty_history]

    plt.plot(iterations, penalties)
    plt.xlabel('Itérations')
    plt.ylabel('Pénalités')
    plt.title('Évolution des pénalités de la recherche locale')
    plt.show()