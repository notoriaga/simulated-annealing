import math
import random
from typing import List, Tuple
from main import score, Flow, Distance, Population


# Globals
STARTING_TEMP = 500.0
ALPHA = 0.99


def gen_population(flow_matrix: Flow, dist_matrix: Distance, n: int) -> Population:
    """ Create n solutions and run SA on them. """

    population = []
    for i in range(n):
        population.append(simmulate_annealing(flow_matrix, dist_matrix))
    return population


def gen_starting_solution(n: int) -> List[int]:
    """ Generates a random permutation. """

    solution = list(range(1, n+1))
    random.shuffle(solution)
    return solution


def swap(permutation: List[int]) -> List[int]:
    """ Swaps two random elements of the permutation - will not
    swap the same one with itself.
    """

    new_perm = list(permutation)
    a, b = random.sample(range(len(new_perm)), 2)
    new_perm[a], new_perm[b] = new_perm[b], new_perm[a]
    return new_perm


def simmulate_annealing(flow_matrix: Flow,
                        dist_matrix: Distance) -> Tuple[List[int], int]:
    """ Simplest version of simmulated annealing at each temp you only run
    one itteration. If the new solution is better take it. Otherwise, pick
    it proportional to the boltzmann function.
    """

    V = gen_starting_solution(len(flow_matrix))
    T = STARTING_TEMP

    while T > 0.01:
        V_prime = swap(V)
        E = score(flow_matrix, dist_matrix, V)
        E_prime = score(flow_matrix, dist_matrix, V_prime)

        if E_prime < E:
            V = V_prime
        else:
            rand = random.uniform(0, 1)
            boltzmann = math.exp((-abs(E - E_prime))/T)
            if boltzmann > rand:
                V = V_prime

        T = T * ALPHA

    return V, score(flow_matrix, dist_matrix, V)
