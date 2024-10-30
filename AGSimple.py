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
    # Randomly mutate a match in the schedule based on the mutation rate
    for week in range(len(schedule)):
        for period in range(len(schedule[week])):
            if random.random() < mutation_rate:  # Apply mutation based on the mutation rate
                if schedule[week][period] is not None:
                    home_team, away_team = schedule[week][period]
                    # Randomly choose to replace either the home or away team
                    if random.random() < 0.5:
                        new_home_team = random.randint(0, num_teams - 1)
                        while new_home_team == home_team:  # Avoid choosing the same team
                            new_home_team = random.randint(0, num_teams - 1)
                        schedule[week][period] = (new_home_team, away_team)
                    else:
                        new_away_team = random.randint(0, num_teams - 1)
                        while new_away_team == away_team:  # Avoid choosing the same team
                            new_away_team = random.randint(0, num_teams - 1)
                        schedule[week][period] = (home_team, new_away_team)

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

        # Create offspring through crossover (5 pairs resulting in 10 offspring)
        while len(offspring) < 6:  # 10 offspring from crossover
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)

        # Create remaining offspring through simple mutation
        while len(offspring) < 30:  # Generate up to 20 offspring
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

