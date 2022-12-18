import sys
import itertools

# Input

lines = [x.strip() for x in sys.stdin.readlines()]
data = []
for line in lines:
    s = line.split(' ')

    name = s[1]
    rate = int(s[4].split('=')[1][:-1])
    connections = s[9:]
    data.append((name, rate, connections))

names = [x[0] for x in data]

# Put input into useful format

data = [(names.index(name), rate, tuple(names.index(x.replace(',', '')) for x in connections))
        for name, rate, connections in data]
NUM_NODES = len(data)
good_nodes = [i for i in range(NUM_NODES) if data[i][1] > 0]
good_nodes.sort(key=lambda i: data[i][1], reverse=True)

# All-pairs shortest path

hub_distance_graph = [[10000000] * NUM_NODES for _ in range(NUM_NODES)]
print(data)

for i in range(NUM_NODES):
    hub_distance_graph[i][i] = 0

changed = True
while changed:
    changed = False
    for i, _, connections in data:
        for j in connections:
            for k in range(NUM_NODES):
                if hub_distance_graph[j][k] > hub_distance_graph[i][k] + 1:
                    hub_distance_graph[j][k] = hub_distance_graph[i][k] + 1
                    changed = True

print(hub_distance_graph)

# Create filtered graph

graph = {k: {v: hub_distance_graph[k][v] + 1
             for v in good_nodes if k != v} for k in good_nodes}
start = names.index('AA')
graph[start] = {
    v: hub_distance_graph[start][v] + 1 for v in good_nodes}

print(graph)

# Find all possible paths of any length

all_paths = set()


def dfs(start, time_left, visited):
    for target, dist in graph[start].items():
        if time_left - dist > 0 and target not in visited:
            new_visited = set(visited)
            new_visited.add(target)

            all_paths.add(tuple(sorted(new_visited)))

            dfs(target, time_left - dist, new_visited)


dfs(start, 26, set())
print(all_paths)

# Compute best weights of each path

all_paths_with_weights = []
for p in all_paths:
    best = 0
    best_path = None
    for path in itertools.permutations(p):
        time_left = 26
        prev = start
        total = 0
        for i in path:
            dist = graph[prev][i]
            rate = data[i][1]
            total += (time_left - dist) * rate
            prev = i
            time_left -= dist
        if total > best:
            best = total
            best_path = path
    all_paths_with_weights.append((best_path, best))

print(all_paths_with_weights)

# Find all compatible pairs of paths

all_compatible_pairs = []

for a in all_paths_with_weights:
    for b in all_paths_with_weights:
        if set(a[0]).isdisjoint(set(b[0])):
            all_compatible_pairs.append((a, b))

# Find best pair

best = 0
for a, b in all_compatible_pairs:
    best = max(best, a[1] + b[1])

print(best)
