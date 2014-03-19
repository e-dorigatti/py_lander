from random import triangular, randint, random, randrange
from simulation import Simulation

class GeneticAlgorithm:
    """
    Genetic algorithm implementation using a sequences of
    floating point numbers as individuals composing the
    population
    """
    def __init__(self, ind_size, pop_size, fitness):
        """
        ind_size is the length of each individual
        pop_size is the count of individuals in the population
        fitness is the fitness function, called as fitness(individual)
        """
        self.population = []
        self.fitness = fitness
        for i in range(pop_size):
            individual = [triangular(0, 100) for j in range(ind_size)]
            self.population.append(individual)

    def probabilistic_choice(self, score_list):
        """
        Chooses an element from scores (a list of tuples)
        with a probability proportional to the first element
        of the tuple.
        """
        cumulatives = [score, score_list[i-1][0] + score, individual
            for score, individual in score_list[1:]]
        choice = randint(0, cumulative[-1][1])

        for score, cumul, individual in cumulatives:
            if cumul > choice:
                return score, individual

    def combine(parent1, parent2):
        """
        Combines two parents using one-point crossover
        and introduce a mutation
        """
        split = randint(0, len(parent1))
        child = parent1[0:split] + parent2[split:]
        if random() < 0.3:
            mutation = randint(0, len(child))
            child[mutation] += triangular(-25, 25)
        return child

    def iteration(self):
        scores = [(self.fitness(individual), individual)
            for individual in self.population]

        new_population = []
        for i in range(len(self.population)):
            fitness1, parent1 = self.probabilistic_choice(scores)
            fitness2, parent2 = self.probabilistic_choice(scores)

            child = self.combine(parent1, parent2)
            new_population.append(child)

        self.population = new_population
        return max([score for score, individual in scores])

def evaluate_controller(controller):
    """
    Gives a score to the controller based on its landing
    performance, determined by the simulation outcome and
    the time elapsed.
    """
    sim = Simulation(controller)
    success, time = sim.simulate()
    if success:
        return time
    else:
        return -(time + 100)

def create_controller(t2, b):
    """
    Creates a parametrized controller behaving as described
    above (free fall --> constant speed --> max thrust).

    a is 90% of max_speed
    t1 is determined according to a
    """
    def controller(sim):
        if sim.time < t2:
            if sim.speed >= sim.max_speed * 0.9:
                return b * 0.01
            else:
                return 0
        else:
            return 1.0

    return controller

def controller_fitness(args):
    t2 = max(0, args[0])
    b = max(0, args[1])
    b = min(b, 100)

    controller = create_controller(t2, b)
    return evaluate_controller(controller)

