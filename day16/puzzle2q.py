import sys
import queue
import threading

NUM_THREADS = 40
lock = threading.Lock()

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
good_nodes = [i for i in range(NUM_NODES) if data[i][1] > 0]
good_nodes.sort(key=lambda i: data[i][1], reverse=True)

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

graph = {k: {v: hub_distance_graph[k][v] + 1
             for v in good_nodes if k != v} for k in good_nodes}
graph[names.index('AA')] = {
    v: hub_distance_graph[names.index('AA')][v] + 1 for v in good_nodes}

print(graph)

best = 0
stack = queue.Queue()
stack.put((names.index('AA'), 26, names.index('AA'), 26, 0, set()))


def calculate():
    global stack
    global best

    while not stack.empty():
        s = stack.get()
        currA, minsA, currB, minsB, total_released, opened = s
        doneMoving = True

        movePlayer = int(minsB > minsA)

        tries = 0
        while True:
            if tries >= 2:
                # We are done
                # print(*s)
                break
            tries += 1

            if movePlayer == 0:
                # Human
                i = currA
                minutes_remaining = minsA

                for j in good_nodes:
                    if i == j:
                        continue
                    dist = graph[i][j]
                # for j, dist in graph[i].items():
                    rate = data[j][1]

                    if minutes_remaining - dist > 0 and j not in opened:
                        new_opened = set(opened)
                        new_opened.add(j)
                        new_released = total_released + \
                            (minutes_remaining - dist) * rate
                        doneMoving = False
                        stack.put((j, minutes_remaining - dist, currB, minsB,
                                   new_released, new_opened))

                if not doneMoving:
                    break
            else:
                # Elephant
                i = currB
                minutes_remaining = minsB

                for j in good_nodes:
                    if i == j:
                        continue
                    dist = graph[i][j]
                # for j, dist in graph[i].items():
                    rate = data[j][1]

                    if minutes_remaining - dist > 0 and j not in opened:
                        new_opened = set(opened)
                        new_opened.add(j)
                        new_released = total_released + \
                            (minutes_remaining - dist) * rate
                        doneMoving = False
                        stack.put((currA, minsA, j, minutes_remaining - dist,
                                   new_released, new_opened))

                if not doneMoving:
                    break

        if doneMoving:
            with lock:
                if total_released > best:
                    best = total_released
                    print(best)
                # print(*s)


threads = []
for _ in range(NUM_THREADS):
    thread = threading.Thread(target=calculate)

    thread.start()

    threads.append(thread)

for t in threads:
    t.join()

print(best)
