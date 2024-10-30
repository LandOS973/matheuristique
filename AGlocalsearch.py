import random
import copy
import fitness
import random_schedule
import local_search_descente


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
    return schedule


def genetic_algorithm(pop_size, num_teams, max_generations, local_search_iterations=100):
    population = create_initial_population(pop_size, num_teams)
    penalty_history = []

    for generation in range(max_generations):
        fitness_scores = evaluate_population(population, num_teams)
        parents = select_top_parents(population, fitness_scores, top_n=5)

        best_penalty = min(fitness_scores)
        penalty_history.append((generation, best_penalty))

        offspring = []

        # Generate 5 offspring using crossover
        while len(offspring) < 6:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)

        # Generate remaining 10 offspring through mutation, followed by local search
        while len(offspring) < 30:
            parent = random.choice(parents)
            mutated_child = copy.deepcopy(parent)
            mutated_child = simple_mutation(mutated_child, num_teams)

            # Apply local search to the mutated child
            mutated_child, penality_mutated, _ = local_search_descente.local_search(mutated_child, num_teams, local_search_iterations)
            offspring.append(mutated_child)

        population = offspring[:pop_size]

    # Final evaluation to select the best individual
    fitness_scores = evaluate_population(population, num_teams)
    best_index = fitness_scores.index(min(fitness_scores))
    best_schedule = population[best_index]
    return best_schedule, fitness_scores[best_index], penalty_history

