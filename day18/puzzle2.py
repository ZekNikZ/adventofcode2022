import sys

data = set(tuple(map(int, line.strip().split(',')))
           for line in sys.stdin.readlines())

# Determine which surfaces are in or out
GRID_SIZE = 25
grid = [[[0] * GRID_SIZE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
# 0 = internal
# 1 = obsidian
# 2 = external
for point in data:
    x, y, z = point
    grid[x][y][z] = 1

# bfs
queue = [(0, 0, 0)]
while len(queue) > 0:
    point = queue.pop(0)
    x, y, z = point

    if grid[x][y][z] > 0:
        continue

    grid[x][y][z] = 2

    if x > 0 and grid[x - 1][y][z] == 0:
        queue.append((x - 1, y, z))
    if y > 0 and grid[x][y - 1][z] == 0:
        queue.append((x, y - 1, z))
    if z > 0 and grid[x][y][z - 1] == 0:
        queue.append((x, y, z - 1))
    if x < GRID_SIZE - 1 and grid[x + 1][y][z] == 0:
        queue.append((x + 1, y, z))
    if y < GRID_SIZE - 1 and grid[x][y + 1][z] == 0:
        queue.append((x, y + 1, z))
    if z < GRID_SIZE - 1 and grid[x][y][z + 1] == 0:
        queue.append((x, y, z + 1))

# Count exposed surfaces
total = 0
for point in data:
    x, y, z = point
    if grid[x - 1][y][z] == 2:
        total += 1
    if grid[x + 1][y][z] == 2:
        total += 1
    if grid[x][y - 1][z] == 2:
        total += 1
    if grid[x][y + 1][z] == 2:
        total += 1
    if grid[x][y][z - 1] == 2:
        total += 1
    if grid[x][y][z + 1] == 2:
        total += 1

print(total)
