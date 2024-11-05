import random
import copy
import fitness
import random_schedule
import local_search_descente
import matplotlib.pyplot as plt


def create_initial_population(pop_size, num_teams):
    population = []
    for _ in range(pop_size):
        schedule = random_schedule.random_round_robin_schedule(num_teams)
        population.append(schedule)
    return population


def evaluate_population(population, num_teams):
    return [fitness.evaluate_schedule(schedule, num_teams, False) for schedule in population]


def select_top_parents(population, fitness_scores, top_n=5, num_teams=12):
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population))]
    # local search sur les top_n
    for i in range(top_n):
        sorted_population[i], penalty, _ = local_search_descente.local_search(sorted_population[i], num_teams, 1000)
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
    population = create_initial_population(pop_size, num_teams)
    penalty_history = []
    lower_penalty = float('inf')
    best_overall_schedule = None  # To store the best schedule across all generations

    for generation in range(max_generations):
        fitness_scores = evaluate_population(population, num_teams)

        # Update best overall schedule and penalty if a better one is found
        generation_best_penalty = min(fitness_scores)
        if generation_best_penalty < lower_penalty:
            lower_penalty = generation_best_penalty
            best_overall_schedule = population[fitness_scores.index(generation_best_penalty)]

        # Store penalty history for plotting
        penalty_history.append((generation, generation_best_penalty))

        parents = select_top_parents(population, fitness_scores, top_n=5, num_teams=num_teams)
        offspring = []

        # Generate offspring through crossover
        while len(offspring) < pop_size // 3:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)
            # Check if these children improve the best overall schedule
            child1_penalty = fitness.evaluate_schedule(child1, num_teams, False)
            child2_penalty = fitness.evaluate_schedule(child2, num_teams, False)
            if child1_penalty < lower_penalty:
                lower_penalty = child1_penalty
                best_overall_schedule = child1
            if child2_penalty < lower_penalty:
                lower_penalty = child2_penalty
                best_overall_schedule = child2

        # Generate remaining offspring through mutation and local search
        while len(offspring) < pop_size:
            parent = random.choice(parents)
            mutated_child = copy.deepcopy(parent)
            mutated_child = simple_mutation(mutated_child, num_teams)
            penalty_mutated = fitness.evaluate_schedule(mutated_child, num_teams, False)
            offspring.append(mutated_child)
            # Check if this mutated child improves the best overall schedule
            if penalty_mutated < lower_penalty:
                lower_penalty = penalty_mutated
                best_overall_schedule = mutated_child

        # Update population for the next generation
        population = offspring[:pop_size]

    # Return the best schedule across all generations and its penalty
    return best_overall_schedule, lower_penalty, penalty_history


if __name__ == "__main__":
    num_teams = 12
    best_schedule, best_penalty, penalty_history = genetic_algorithm(20, num_teams, 300)
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
