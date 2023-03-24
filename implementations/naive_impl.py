def entry(A):
    cycles = set()
    for vertex, neighbors in enumerate(A):
        for neighbor, value in enumerate(neighbors):
            if value > 0:
                for third_neighbor in range(len(A)):
                    if A[neighbor][third_neighbor] > 0 and A[third_neighbor][vertex] > 0:
                        candidate = frozenset((vertex, neighbor, third_neighbor))
                        cycles.add(candidate)
    return cycles
