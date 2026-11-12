"""Genetic Algorithm for hourly TV scheduling (repeated programs permitted)."""
import csv
import random
from pathlib import Path


def load_ratings(path):
    with open(path, newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        header = next(reader)
        hours = [int(h.replace('Hour ', '')) for h in header[1:]]
        ratings = {}
        for row in reader:
            if not row:
                continue
            if len(row) != len(hours) + 1:
                raise ValueError(f'Incorrect number of ratings for {row[0]}')
            ratings[row[0]] = [float(value) for value in row[1:]]
    if not ratings or not hours:
        raise ValueError('Ratings dataset is empty')
    return hours, ratings


def fitness(schedule, ratings):
    return sum(ratings[program][index] for index, program in enumerate(schedule))


def tournament_select(population, ratings, rng, k=3):
    candidates = rng.sample(population, min(k, len(population)))
    return max(candidates, key=lambda s: fitness(s, ratings))


def crossover(a, b, rng):
    point = rng.randint(1, len(a) - 1)
    return a[:point] + b[point:], b[:point] + a[point:]


def mutate(schedule, programs, rng):
    result = schedule.copy()
    index = rng.randrange(len(result))
    alternatives = [p for p in programs if p != result[index]]
    if alternatives:
        result[index] = rng.choice(alternatives)
    return result


def genetic_algorithm(ratings, crossover_rate=0.8, mutation_rate=0.02,
                      generations=100, population_size=50, elitism_size=2, seed=42):
    if not 0 <= crossover_rate <= 0.95:
        raise ValueError('Crossover rate must be 0–0.95')
    if not 0.01 <= mutation_rate <= 0.05:
        raise ValueError('Mutation rate must be 0.01–0.05')
    if population_size < 4 or not 1 <= elitism_size < population_size:
        raise ValueError('Invalid population/elitism sizes')
    if generations < 1:
        raise ValueError('Generations must be positive')
    rng = random.Random(seed)
    programs = list(ratings)
    n_slots = len(next(iter(ratings.values())))
    population = [[rng.choice(programs) for _ in range(n_slots)] for _ in range(population_size)]
    history = []
    for _ in range(generations):
        population.sort(key=lambda s: fitness(s, ratings), reverse=True)
        history.append(fitness(population[0], ratings))
        next_population = [s.copy() for s in population[:elitism_size]]
        while len(next_population) < population_size:
            a = tournament_select(population, ratings, rng)
            b = tournament_select(population, ratings, rng)
            if rng.random() < crossover_rate:
                a, b = crossover(a, b, rng)
            else:
                a, b = a.copy(), b.copy()
            if rng.random() < mutation_rate:
                a = mutate(a, programs, rng)
            if rng.random() < mutation_rate:
                b = mutate(b, programs, rng)
            next_population.extend([a, b][:population_size - len(next_population)])
        population = next_population
    population.sort(key=lambda s: fitness(s, ratings), reverse=True)
    best = population[0]
    history.append(fitness(best, ratings))
    return best, fitness(best, ratings), history
