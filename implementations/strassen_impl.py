import sys
import math

def operation(A, B, fn):
    if isinstance(A, int):
        return fn(A, B)

    result = [[0]*len(A[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = fn(A[i][j], B[i][j])
    return result

def add(A, B):
    return operation(A, B, lambda a, b: a + b)

def sub(A, B):
    return operation(A, B, lambda a, b: a - b)

def convert(A):
    n = len(A)
    small_size = n // 2

    A11 = [A[i][:small_size] for i in range(small_size)]
    A12 = [A[i][small_size:] for i in range(small_size)]
    A21 = [A[i][:small_size] for i in range(small_size, n)]
    A22 = [A[i][small_size:] for i in range(small_size, n)]

    return [[A11, A12], [A21, A22]]

def restore(C11, C12, C21, C22, original_size):

    small_size = original_size // 2

    result = [[0] * original_size for i in range(original_size)]
    for y in range(small_size):
        for x in range(small_size):
            result[y][x] = C11[y][x]
            result[y][x + small_size] = C12[y][x]
            result[y + small_size][x] = C21[y][x]
            result[y + small_size][x + small_size] = C22[y][x]
    return result

def strassen(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A = convert(A)
    B = convert(B)

    S1 = sub(B[0][1], B[1][1])
    S2 = add(A[0][0], A[0][1])
    S3 = add(A[1][0], A[1][1])
    S4 = sub(B[1][0], B[0][0])
    S5 = add(A[0][0], A[1][1])
    S6 = add(B[0][0], B[1][1])
    S7 = sub(A[0][1], A[1][1])
    S8 = add(B[1][0], B[1][1])
    S9 = sub(A[1][0], A[0][0])
    S10 = add(B[0][0], B[0][1])

    P1 = strassen(A[0][0], S1)
    P2 = strassen(S2, B[1][1])
    P3 = strassen(S3, B[0][0])
    P4 = strassen(A[1][1], S4)
    P5 = strassen(S5, S6)
    P6 = strassen(S7, S8)
    P7 = strassen(S9, S10)

    C11 = add(sub(add(P5, P4), P2), P6)
    C12 = add(P1, P2)
    C21 = add(P3, P4)
    C22 = add(sub(add(P5, P1), P3), P7)

    return restore(C11, C12, C21, C22, n)


def expand_horizontally(A, size):
    n = len(A[0])
    if size > n:
        for i in range(len(A)):
            A[i].extend([0 for i in range(size - n)])

def expand_vertically(A, size):
    if size > len(A):
        for i in range(size - len(A)):
            A.append([0 for i in range(size)])

def shrink(A, row, col):
    n = len(A)
    if n > row:
        A = A[:row]
    if len(A[0]) > col:
        for i in range(row):
            A[i] = A[i][:col]
    return A

def mul(A, B):
    rows_A = len(A)
    cols_A = len(A[0])

    rows_B = len(B)
    cols_B = len(B[0])

    max_val = max(max(max(rows_A, cols_A), rows_B), cols_B)
    new_val = 2**math.ceil(math.log(max_val, 2))

    expand_horizontally(A, new_val)
    expand_horizontally(B, new_val)

    expand_vertically(A, new_val)
    expand_vertically(B, new_val)

    result = strassen(A, B)
    A = shrink(A, rows_A, cols_A)
    return A, shrink(result, rows_A, cols_B)

def find_common_neighbors(A, vertA, vertB, undirected):
    results = []
    if undirected:
        for neighbor, value in enumerate(A[vertA]):
            if value > 0 and A[vertB][neighbor] > 0:
                results.append(neighbor)
    else:
        for neighbor, value in enumerate(A[vertB]):
            if value > 0 and A[neighbor][vertA] > 0:
                results.append(neighbor)
    return results

def entry(matA):
    matA, multipliedA = mul(matA, matA)
    cycles = set()
    for vertex, neighbors in enumerate(matA):
        for neighbor, value in enumerate(neighbors):
            if vertex != neighbor and value > 0 and ((multipliedA[vertex][neighbor] > 0 and matA[neighbor][value]) or multipliedA[neighbor][vertex] > 0):
                undirected = matA[neighbor][value] > 0
                common_neighbors = find_common_neighbors(matA, vertex, neighbor, undirected)
                for common_neighbor in common_neighbors:
                    candidate = frozenset((vertex, neighbor, common_neighbor))
                    cycles.add(candidate)
    return cycles
