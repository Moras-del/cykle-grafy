import time
import sys
import random

from implementations.naive_impl import entry as naive_entry
from implementations.dfs_impl import entry as dfs_entry
from implementations.strassen_impl import entry as strassen_entry

ITERS_PER_METHOD = 1000
N = 8


def naive(matrix):
    return naive_entry(matrix)

def dfs(matrix):
    return dfs_entry(matrix)

def strassen(matrix):
    return strassen_entry(matrix)

def generate_matrix(n):
    result = [[1]*n for i in range(n)]
    for y in range(n):
        for x in range(n):
            if y == x:
                continue
            result[y][x] = random.randint(0, 1)
    return result

def run_tests(matrix, implementations):
    result = None
    for implementation in implementations:
        total_time = 0
        for iteration in range(ITERS_PER_METHOD):
            start = time.time()
            curr_result = implementation(matrix)
            end = time.time()
            total_time += (end - start) 
            if iteration == 0:
                result = curr_result
            else:
                assert(result == curr_result) # sprawdź czy wyniki są zawsze takie same (algorytm jest deterministyczny)
        avg_time = total_time / ITERS_PER_METHOD
        print(f'{implementation.__name__}: średnio {avg_time} sekund')


if __name__ == '__main__':
    print('Pierwszy argument dla liczby iteracji, drugi dla rozmiaru macierzy')
    if len(sys.argv) == 2:
        ITERS_PER_METHOD = int(sys.argv[1])
    else:
        ITERS_PER_METHOD = int(sys.argv[1])
        N = int(sys.argv[2])
    matrix = generate_matrix(N)
    implementations = [naive, dfs, strassen]
    run_tests(matrix, implementations)

