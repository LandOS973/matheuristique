import random
import copy
import fitness
import random_schedule  # Ensure this is correctly implemented

def create_initial_population(pop_size, num_teams):
    population = []
    for _ in range(pop_size):
        # Generate a random round-robin schedule
        schedule = random_schedule.random_round_robin_schedule(num_teams)
        population.append(schedule)
    return population

def evaluate_population(population, num_teams):
    return [fitness.evaluate_schedule(schedule, num_teams, False) for schedule in population]

def select_top_parents(population, fitness_scores, top_n=5):
    # Select the top N parents based on their fitness scores (lower scores are better)
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population))]
    return sorted_population[:top_n]  # Return the top N schedules

def crossover(parent1, parent2):
    # One-point crossover
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
                    if random.random() < 0.3:
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

def genetic_algorithm(pop_size, num_teams, max_generations):
    # Create an initial population
    population = create_initial_population(pop_size, num_teams)
    penalty_history = []  # To store penalty history at each generation

    for generation in range(max_generations):
        # Evaluate the fitness of the population
        fitness_scores = evaluate_population(population, num_teams)

        # Select the top 5 parents
        parents = select_top_parents(population, fitness_scores, top_n=5)

        # Track the best penalty for this generation
        best_penalty = min(fitness_scores)
        penalty_history.append((generation, best_penalty))

        offspring = []

        while len(offspring) < pop_size//5:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)

        # Create remaining offspring through simple mutation
        while len(offspring) < pop_size:  # Generate up to 20 offspring
            # Select a random parent and mutate it
            parent = random.choice(parents)
            mutated_child = copy.deepcopy(parent)  # Deep copy to avoid modifying the parent
            simple_mutation(mutated_child, num_teams)  # Mutate the child
            offspring.append(mutated_child)

        # Replace the existing population with the new offspring
        population = offspring[:pop_size]  # Keep the population size consistent

    # Return the best schedule found and the penalty history
    fitness_scores = evaluate_population(population, num_teams)
    best_index = fitness_scores.index(min(fitness_scores))
    best_schedule = population[best_index]
    return best_schedule, fitness_scores[best_index], penalty_history

import time
import matplotlib.pyplot as plt

def test_genetic_algo_with_different_pop_sizes(num_teams, max_generations):
    pop_sizes = range(10, 350, 5)
    results = []
    for pop_size in pop_sizes:
        start_time = time.time()  # Démarrer le chronomètre
        best_schedule, best_penalty, _ = genetic_algorithm(pop_size, num_teams, max_generations)
        execution_time = time.time() - start_time  # Calculer le temps d'exécution
        results.append([pop_size, best_penalty, execution_time])
        print(f"Population Size: {pop_size}, Best Penalty: {best_penalty}, Execution Time: {execution_time:.4f} seconds")
    return results


if __name__ == "__main__":
    num_teams = 12
    max_generations = 300
    results = test_genetic_algo_with_different_pop_sizes(num_teams, max_generations)

    # Séparer les tailles de populations, les pénalités et les temps d'exécution
    pop_sizes, penalties, execution_times = zip(*results)

    # Trouver l'indice du score de fitness le plus faible
    min_index = penalties.index(min(penalties))
    min_pop_size = pop_sizes[min_index]
    min_penalty = penalties[min_index]

    # Tracer la courbe des pénalités en fonction des tailles de population
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(pop_sizes, penalties, label='Score de fitness')
    plt.xlabel('Population')
    plt.ylabel('Score fitness')
    plt.title('Algo génétique simple : Influence de la taille de la population avec 12 équipes')
    plt.plot(min_pop_size, min_penalty, 'rX', markersize=10, label='Score minimum')
    plt.legend()

    # Tracer la courbe des temps d'exécution en fonction des tailles de population
    plt.subplot(1, 2, 2)
    plt.plot(pop_sizes, execution_times, label='Temps d\'exécution', color='orange')
    plt.xlabel('Population')
    plt.ylabel('Temps d\'exécution (s)')
    plt.title('Algo génétique : Temps d\'exécution en fonction de la taille de population')
    plt.legend()

    # Afficher les deux graphiques
    plt.tight_layout()
    plt.show()






