import random
import copy
import fitness
import random_schedule
import local_search_descente
import matplotlib.pyplot as plt

from simulated_annealing import simulated_annealing


def create_initial_population(pop_size, num_teams):
    population = []
    for _ in range(pop_size):
        schedule = random_schedule.random_round_robin_schedule(num_teams)
        population.append(schedule)
    return population


def evaluate_population(population, num_teams):
    return [fitness.evaluate_schedule(schedule, num_teams, False) for schedule in population]


def select_top_parents(population, fitness_scores, top_n=5):
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population))]
    return sorted_population[:top_n]


def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = copy.deepcopy(parent1[:crossover_point]) + parent2[crossover_point:]
    child2 = copy.deepcopy(parent2[:crossover_point]) + parent1[crossover_point:]
    return child1, child2


def simple_mutation(schedule, num_teams, mutation_rate=0.1):
    for week in range(len(schedule)):
        for period in range(len(schedule[week])):
            if random.random() < mutation_rate:
                if schedule[week][period] is not None:
                    home_team, away_team = schedule[week][period]
                    if random.random() < 0.4:
                        if random.random() < 0.5:
                            new_home_team = random.randint(0, num_teams - 1)
                            while new_home_team == home_team:
                                new_home_team = random.randint(0, num_teams - 1)
                            schedule[week][period] = (new_home_team, away_team)
                        else:
                            new_away_team = random.randint(0, num_teams - 1)
                            while new_away_team == away_team:
                                new_away_team = random.randint(0, num_teams - 1)
                            schedule[week][period] = (home_team, new_away_team)
                    else:
                        # Swap 2 matches
                        week1, period1 = random.randint(0, len(schedule) - 1), random.randint(0, len(schedule[0]) - 1)
                        week2, period2 = random.randint(0, len(schedule) - 1), random.randint(0, len(schedule[0]) - 1)
                        stock1 = schedule[week1][period1]
                        stock2 = schedule[week2][period2]
                        schedule[week1][period1] = stock2
                        schedule[week2][period2] = stock1
    return schedule


def genetic_algorithm(pop_size, num_teams, max_generations, verbose=False):
    population = create_initial_population(pop_size, num_teams)
    penalty_history = []
    lower_penalty = float('inf')
    best_overall_schedule = None  # Pour stocker le meilleur planning de toutes les générations

    stuck = 0

    for generation in range(max_generations):
        fitness_scores = evaluate_population(population, num_teams)

        # Mettre à jour le meilleur planning global et la pénalité si un meilleur est trouvé
        generation_best_penalty = min(fitness_scores)
        if generation_best_penalty < lower_penalty:
            lower_penalty = generation_best_penalty
            best_overall_schedule = population[fitness_scores.index(generation_best_penalty)]

        # Stocker l'historique des pénalités pour les graphiques
        penalty_history.append((generation, generation_best_penalty))

        # Sélection des meilleurs parents
        parents = select_top_parents(population, fitness_scores, top_n=5)
        offspring = []

        stuck += 1

        if stuck > 100:
            break

        if verbose:
            print(f"Generation {generation}: Meilleure pénalité {lower_penalty}")

        # Génération de la descendance par croisement
        while len(offspring) < pop_size // 6:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)
            # Vérifier si ces enfants améliorent le meilleur planning global
            child1_penalty = fitness.evaluate_schedule(child1, num_teams, False)
            child2_penalty = fitness.evaluate_schedule(child2, num_teams, False)
            if child1_penalty < lower_penalty:
                lower_penalty = child1_penalty
                best_overall_schedule = child1
                stuck = 0
            if child2_penalty < lower_penalty:
                lower_penalty = child2_penalty
                best_overall_schedule = child2
                stuck = 0

        # Génération de la descendance restante par mutation
        while len(offspring) < pop_size:
            parent = random.choice(parents)
            mutated_child = copy.deepcopy(parent)
            mutated_child = simple_mutation(mutated_child, num_teams)
            penalty_mutated = fitness.evaluate_schedule(mutated_child, num_teams, False)
            offspring.append(mutated_child)
            # Vérifier si cet enfant muté améliore le meilleur planning global
            if penalty_mutated < lower_penalty:
                lower_penalty = penalty_mutated
                best_overall_schedule = mutated_child
                stuck = 0

        # Mettre à jour la population pour la prochaine génération
        population = offspring[:pop_size]

        # Appliquer le recuit simulé aux 3 meilleurs plannings de la génération actuelle
        fitness_scores = evaluate_population(population, num_teams)
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population))]
        best_schedules = sorted_population[:3]

        for i in range(3):
            improved_schedule, penalty, _ = local_search_descente.local_search(best_schedules[i], num_teams, max_iterations=300, verbose=False)
            if penalty < fitness_scores[i]:  # Si le score s'améliore
                population[i] = improved_schedule  # Remplace dans la population
                if penalty < lower_penalty:  # Si c'est le meilleur global
                    lower_penalty = penalty
                    best_overall_schedule = improved_schedule
                    stuck = 0

    # Retourner le meilleur planning global et sa pénalité
    return best_overall_schedule, lower_penalty, penalty_history


if __name__ == "__main__":
    num_teams = 12
    best_schedule, best_penalty, penalty_history = genetic_algorithm(200, num_teams, 1000, verbose=True)
    print(f"Score de la planification (pénalités totales): {best_penalty}")
    print("Meilleur schedule:", best_schedule)

    # Plot the evolution of penalties
    generations = [entry[0] for entry in penalty_history]
    penalties = [entry[1] for entry in penalty_history]

    plt.plot(generations, penalties)
    plt.xlabel('Générations')
    plt.ylabel('Pénalités')
    plt.title("Évolution des pénalités dans l'algorithme génétique")
    plt.show()
