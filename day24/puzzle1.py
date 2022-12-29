import sys
import math

grid = [list(l.strip()) for l in sys.stdin]
GRID_WIDTH = len(grid[0])
GRID_HEIGHT = len(grid)

blizzard_states = []


def get_blizzard_state(t):
    while t >= len(blizzard_states):
        blizzards = set()
        for r, c, dir in blizzard_states[-1]:
            if dir == '>':
                dr = 0
                dc = 1
            elif dir == '<':
                dr = 0
                dc = -1
            elif dir == 'v':
                dr = 1
                dc = 0
            else:
                dr = -1
                dc = 0
            new_r = r + dr
            if new_r <= 0:
                new_r = GRID_HEIGHT - 2
            elif new_r >= GRID_HEIGHT - 1:
                new_r = 1
            new_c = c + dc
            if new_c <= 0:
                new_c = GRID_WIDTH - 2
            elif new_c >= GRID_WIDTH - 1:
                new_c = 1
            blizzards.add((new_r, new_c, dir))
        blizzard_states.append(blizzards)

    # print(f'Generated blizzard states up to t={len(blizzard_states) - 1}')
    return blizzard_states[t]


def search_blizzards(blizzards, r, c):
    for b in blizzards:
        if b[0] == r and b[1] == c:
            return True

    return False


# Construct initial blizzard state
blizzards = set()
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] != '.' and grid[r][c] != '#':
            blizzards.add((r, c, grid[r][c]))
blizzard_states.append(blizzards)

# Generate a lot of blizzard states to make search a little faster
get_blizzard_state(math.lcm(GRID_WIDTH, GRID_HEIGHT) + 2)
print('Done generating blizzards')

# Make queue
# Entries are (taxicab distance from end, r, c, t)
possible_spots = set()
possible_spots.add((0, 1))

# Perform search
for t in range(1, 100000):
    # print(t, possible_spots)
    new_possibles = set()

    if (GRID_HEIGHT - 1, GRID_WIDTH - 2) in possible_spots:
        print(t)
        break

    next_blizzards = get_blizzard_state(t + 1)

    for r, c in possible_spots:
        # Check if we can stand still
        if not search_blizzards(next_blizzards, r, c):
            new_possibles.add((r, c))

        # Check if we can move down
        if r + 1 < GRID_HEIGHT - 1 and not search_blizzards(next_blizzards, r + 1, c):
            new_possibles.add((r + 1, c))
        elif c == GRID_WIDTH - 2 and r + 1 < GRID_HEIGHT and not search_blizzards(next_blizzards, r + 1, c):
            new_possibles.add((r + 1, c))

        # Check if we can move right
        if r > 0 and c + 1 < GRID_WIDTH - 1 and not search_blizzards(next_blizzards, r, c + 1):
            new_possibles.add((r, c + 1))

        # Check if we can move up
        if r - 1 > 0 and not search_blizzards(next_blizzards, r - 1, c):
            new_possibles.add((r - 1, c))

        # Check if we can move left
        if c - 1 > 0 and not search_blizzards(next_blizzards, r, c - 1):
            new_possibles.add((r, c - 1))

    possible_spots = new_possibles
