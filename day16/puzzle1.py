import sys

lines = [x.strip() for x in sys.stdin.readlines()]
data = []
for line in lines:
    s = line.split(' ')

    name = s[1]
    rate = int(s[4].split('=')[1][:-1])
    connections = s[9:]
    data.append((name, rate, connections))

names = [x[0] for x in data]

data = [(names.index(name), rate, tuple(names.index(x.replace(',', '')) for x in connections))
        for name, rate, connections in data]
NUM_NODES = len(data)

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

best = 0
stack = [(names.index('AA'), 30, 0, [])]
xxx = [3, 1, 9, 7, 4, 2]
while len(stack) > 0:
    current, minutes_remaining, total_released, opened = stack.pop(0)
    doneMoving = True

    i, _, connections = data[current]

    for j in range(NUM_NODES):
        _, rate, _ = data[j]
        if i == j or rate == 0:
            continue

        dist = hub_distance_graph[i][j] + 1

        if minutes_remaining - dist > 0 and j not in opened:
            new_opened = opened[:]
            new_opened.append(j)
            new_released = total_released + \
                (minutes_remaining - dist) * rate
            doneMoving = False
            stack.append((j, minutes_remaining - dist,
                         new_released, new_opened))

    if doneMoving:
        if total_released > best:
            best = total_released

print(best)
