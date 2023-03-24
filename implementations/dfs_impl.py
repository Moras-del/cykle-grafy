def entry(graph):
    cycles = set()
    for vertex in range(len(graph)):
        visited = [False] * len(graph)

        stack = [vertex]
        visited[vertex] = True
        parent_tracker = dict()

        while len(stack) > 0:
            curr = stack.pop()
            for neighbor, value in enumerate(graph[curr]):
                if value > 0 and not visited[neighbor]:
                    visited[neighbor] = True
                    parent_tracker[neighbor] = curr
                    stack.append(neighbor)
                elif curr in parent_tracker:
                    if value > 0 and graph[neighbor][parent_tracker[curr]] > 0:
                        cycles.add(frozenset((curr, neighbor, parent_tracker[curr])))
    return cycles


# 0 3 6
