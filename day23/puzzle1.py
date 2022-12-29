import sys
from collections import defaultdict

NUM_ROUNDS = 10

grid = [l.strip() for l in sys.stdin]

elves = set()
for row in range(len(grid)):
    for col in range(len(grid[row])):
        if grid[row][col] == '#':
            elves.add((row, col))

options = [
    # North
    lambda r, c: ((r - 1, c - 1) not in elves and (r - 1, c)
                  not in elves and (r - 1, c + 1) not in elves, (r - 1, c)),
    # South
    lambda r, c: ((r + 1, c - 1) not in elves and (r + 1, c)
                  not in elves and (r + 1, c + 1) not in elves, (r + 1, c)),
    # West
    lambda r, c: ((r - 1, c - 1) not in elves and (r, c - 1)
                  not in elves and (r + 1, c - 1) not in elves, (r, c - 1)),
    # East
    lambda r, c: ((r - 1, c + 1) not in elves and (r, c + 1)
                  not in elves and (r + 1, c + 1) not in elves, (r, c + 1)),
]

for round_number in range(NUM_ROUNDS):
    # First-half
    considered_where_tos = {}
    considered_positions = defaultdict(list)
    for elf in elves:
        x, y = elf
        # Check surrounding
        surroundings_clear = True
        for xx in range(x - 1, x + 2):
            for yy in range(y - 1, y + 2):
                if xx == x and yy == y:
                    continue
                if (xx, yy) in elves:
                    surroundings_clear = False
                    break

        if surroundings_clear:
            continue

        # Check directions
        for i in range(4):
            can_move, where_to = options[(i + round_number) % 4](*elf)
            if can_move:
                considered_positions[where_to].append(elf)
                considered_where_tos[elf] = where_to
                break

    # Second-half
    new_elves = set()
    for elf in elves:
        where_to = considered_where_tos.get(elf)
        if where_to is not None and len(considered_positions[where_to]) == 1:
            new_elves.add(where_to)
        else:
            new_elves.add(elf)
    elves = new_elves

# Compute rectangle
min_x = 1000000000
min_y = 1000000000
max_x = -1000000000
max_y = -1000000000
for x, y in elves:
    if x < min_x:
        min_x = x
    if x > max_x:
        max_x = x
    if y < min_y:
        min_y = y
    if y > max_y:
        max_y = y

# Compute result
res = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)
print(res)
