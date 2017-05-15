import anneal
import time
from typing import List, Tuple


# Type aliases
Flow = List[List[int]]
Distance = List[List[int]]
Population = List[Tuple[List[int], int]]

#Globals
POP_SIZE = 20


def score(flow_matrix: Flow,
          dist_matrix: Distance,
          permutation: List[int]) -> int:
    """ Returns the cost of a solution """

    n = len(flow_matrix)
    score = 0
    for i in range(n):
        for j in range(n):
            d_i = permutation[i] - 1
            d_j = permutation[j] - 1
            score += flow_matrix[i][j] * dist_matrix[d_i][d_j]
    return score


def load_problem_instance(fpath: str) -> Tuple[Flow, Distance]:
    """ Load problems of the form
    n
    \n
    A
    \n
    B
    where A is the flow matrix and B is the distance matrix.
    """

    f = open(fpath)
    n = int(f.readline())

    f.readline()
    flow_matrix = []
    for i in range(n):
        flow_matrix.append(list(map(int, f.readline().split())))

    f.readline()
    dist_matrix = []
    for i in range(n):
        dist_matrix.append(list(map(int, f.readline().split())))

    return flow_matrix, dist_matrix


def load_optimal_solution(fpath: str) -> Tuple[int, List[int]]:
    f = open(fpath)
    n, opt_score = list(map(int, f.readline().strip().split()))
    opt_perm = list(map(int, f.readline().split()))
    return opt_score, opt_perm


def main() -> None:
    test_cases = [('n18.txt', 'n18_sol.txt'),('n25.txt', 'n25_sol.txt'), ('n50.txt', 'n50_sol.txt')]
    for case in test_cases:
        start = time.time()
        flow_matrix, dist_matrix = load_problem_instance(case[0])
        opt_score, opt_perm = load_optimal_solution(case[1])
        population = anneal.gen_population(flow_matrix, dist_matrix, POP_SIZE)
        best = min(population, key=lambda x: x[1])
        end = time.time()
        print('n = {}'.format(len(flow_matrix)))
        print('Approximate Solution: ', best[0], best[1])
        print('Known Optimal:        ', opt_perm, opt_score)
        print('{} percent within optimal in {} seconds.'.format(opt_score/best[1],end-start))
        print()


if __name__ == '__main__':
    main()
