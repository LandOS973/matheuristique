# main.py

import fitness
import glouton
import random_schedule
import local_search_descente
import matplotlib.pyplot as plt
import time

# Fonction d'affichage pour la planification
import matplotlib.pyplot as plt
import numpy as np

# Fonction d'affichage pour la planification
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

import time  # Pour mesurer le temps d'exécution

def mean_score(algo='glouton'):
    # Nombre d'itérations
    it = 200
    sum_fitness = 0  # Pour stocker la somme des scores de fitness
    total_time = 0   # Pour stocker la somme des temps d'exécution

    print("Calcul de la moyenne pour " + algo + " sur " + str(it) + " itérations")

    for i in range(it):
        start_time = time.time()  # Démarre le chronomètre pour l'itération

        if algo == 'glouton':
            schedule = glouton.round_robin_schedule(8)
        elif algo == 'random':
            schedule = random_schedule.random_round_robin_schedule(8)
        elif algo == 'local_search_random':
            schedule = local_search_descente.local_search(random_schedule.random_round_robin_schedule(8), 8, max_iterations=600, verbose=False)[0]
        elif algo == 'local_search_glouton':
            schedule = local_search_descente.local_search(glouton.round_robin_schedule(8), 8, max_iterations=600, verbose=False)[0]

        # Calculer le score de fitness
        sum_fitness += fitness.evaluate_schedule(schedule, 8, False)

        end_time = time.time()  # Arrête le chronomètre
        total_time += (end_time - start_time)  # Ajoute le temps écoulé à la somme totale

    # Moyenne des scores et des temps
    mean_fitness = sum_fitness / it
    mean_time = total_time / it

    print(f"Temps moyen d'exécution pour {algo}: {mean_time:.5f} secondes")
    print(f"Score moyen de fitness pour {algo}: {mean_fitness:.5f}")

    return mean_fitness, mean_time

            


def main():
    num_teams = 8
    
    # glouton 
    scheduleGlouton = glouton.round_robin_schedule(num_teams)
    penaltyGlouton = fitness.evaluate_schedule(scheduleGlouton, num_teams, False)
    print("\n")
    print(f"GLOUTON : Score de la planification (pénalités totales): {penaltyGlouton}")
    print_schedule(scheduleGlouton)
    
    # random
    scheduleRandom = random_schedule.random_round_robin_schedule(num_teams)
    penaltyRandom = fitness.evaluate_schedule(scheduleRandom, num_teams, False)
    print("\n")
    print(f"RANDOM : Score de la planification (pénalités totales): {penaltyRandom}")
    print_schedule(scheduleRandom)

    # recherche locale
    scheduleLocal, penaltyLocal, penalty_history = local_search_descente.local_search(scheduleRandom, num_teams, max_iterations=600, verbose=True)
    print("\n")
    print(f"RECHERCHE LOCALE : Score de la planification (pénalités totales): {penaltyLocal}")
    print_schedule(scheduleLocal)
    # Pour tracer les pénalités
    
    
    iterations = [entry[0] for entry in penalty_history]
    penalties = [entry[1] for entry in penalty_history]
    
    plt.plot(iterations, penalties)
    plt.xlabel('Itérations')
    plt.ylabel('Pénalités')
    plt.title('Évolution des pénalités de la recherche locale a partir d\'un random')
    plt.show()
    
    # Comparaison des algorithmes
    mean_score('glouton')
    mean_score('random')
    mean_score('local_search_random')
    mean_score('local_search_glouton')

    
if __name__ == "__main__":
    main()
