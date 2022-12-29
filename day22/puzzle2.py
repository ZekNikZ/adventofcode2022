import sys


def net_cell_of(grid, row, col):
    # This is hand-computed
    if 1 <= row <= 50 and 51 <= col <= 100:
        return 0
    elif 1 <= row <= 50 and 101 <= col <= 150:
        return 1
    elif 51 <= row <= 100 and 51 <= col <= 100:
        return 2
    elif 101 <= row <= 150 and 51 <= col <= 100:
        return 3
    elif 101 <= row <= 150 and 1 <= col <= 50:
        return 4
    elif 151 <= row <= 200 and 1 <= col <= 50:
        return 5

    return None


def index(list: str, val):
    try:
        return list.index(val)
    except ValueError:
        return 1000000000


def rindex(list: str, val):
    try:
        return list.rindex(val)
    except ValueError:
        return 0


grid: list[str] = []
raw_instructions: str = None

# Read input
for line in sys.stdin:
    if line.strip() == '':
        break
    # Extra padding so that I don't need to worry about checking for out of bounds when wrapping around
    grid.append(' ' + line[:-1] + ' ')
raw_instructions = input()

# Pad every line to be same length
max_len = max(map(len, grid))
grid = [line.ljust(max_len) for line in grid]

# More extra padding
grid.append(' ' * len(grid[0]))
grid.insert(0, ' ' * len(grid[0]))

# DEBUG
print(*(''.join(grid[r][c] if net_cell_of(grid, r, c) is None else str(net_cell_of(grid, r, c)) for c in range(len(grid[0])))
      for r in range(len(grid))), sep='\n')

# Compute flipped grid
output_grid = [list(l) for l in grid]
flipped_grid = list(''.join(l) for l in zip(*grid))

# Starting location
row: int = 1
col: int = grid[1].index('.')
direction: int = 0  # 0 = right, 1 = down, 2 = left, 3 = up
output_grid[row][col] = '>'

# Parse instructions
instructions: list[str] = []
l = 0
for i in range(len(raw_instructions)):
    if raw_instructions[i].isalpha():
        instructions.append(raw_instructions[l:i])
        l = i + 1
        instructions.append(raw_instructions[i])
instructions.append(raw_instructions[l:])

# Start navigating
for i, instruction in enumerate(instructions):
    should_print = False
    already_printed = set()
    if instruction == 'R':
        direction = (direction + 1) % 4
        output_grid[row][col] = ['>', 'v', '<', '^'][direction]
    elif instruction == 'L':
        direction = (direction - 1) % 4
        output_grid[row][col] = ['>', 'v', '<', '^'][direction]
    else:
        steps = int(instruction)
        for _ in range(steps):
            # Determine delta
            if direction == 0:
                dr = 0
                dc = 1
            elif direction == 1:
                dr = 1
                dc = 0
            elif direction == 2:
                dr = 0
                dc = -1
            else:
                dr = -1
                dc = 0

            # Check for wrap-around
            new_direction = None
            if grid[row + dr][col + dc] == ' ':
                from_cell = net_cell_of(grid, row, col)
                from_direction = direction
                if from_cell == 0 and direction == 2:
                    new_row = (50 - row) + 101
                    new_col = 1
                    new_direction = 0
                elif from_cell == 5 and direction == 0:
                    new_row = 150
                    new_col = row - 151 + 51
                    new_direction = 3
                elif from_cell == 2 and direction == 2:
                    new_row = 101
                    new_col = row - 51 + 1
                    new_direction = 1
                elif from_cell == 3 and direction == 0:
                    new_row = (150 - row) + 1
                    new_col = 150
                    new_direction = 2
                elif from_cell == 1 and direction == 1:
                    new_row = (col - 101) + 51
                    new_col = 100
                    new_direction = 2
                elif from_cell == 1 and direction == 0:
                    new_row = (50 - row) + 101
                    new_col = 100
                    new_direction = 2
                elif from_cell == 2 and direction == 0:
                    new_row = 50
                    new_col = (row - 51) + 101
                    new_direction = 3
                elif from_cell == 0 and direction == 3:
                    new_row = (col - 51) + 151
                    new_col = 1
                    new_direction = 0
                elif from_cell == 5 and direction == 1:
                    new_row = 1
                    new_col = (col - 1) + 101
                    new_direction = 1
                elif from_cell == 1 and direction == 3:
                    new_row = 200
                    new_col = (col - 101) - 1
                    new_direction = 3
                elif from_cell == 3 and direction == 1:
                    new_row = (col - 51) + 151
                    new_col = 50
                    new_direction = 2
                elif from_cell == 5 and direction == 2:
                    new_row = 1
                    new_col = (row - 151) + 51
                    new_direction = 1
                elif from_cell == 4 and direction == 2:
                    new_row = (150 - row) + 1
                    new_col = 51
                    new_direction = 0
                elif from_cell == 4 and direction == 3:
                    new_row = (col - 1) + 51
                    new_col = 51
                    new_direction = 0
                else:
                    raise ValueError(
                        f'({i} / {len(instructions)}) Edge case not handled from cell {from_cell} ({row}, {col}) with direction {direction}')
                dr = new_row - row
                dc = new_col - col
                # if (from_cell, from_direction) not in already_printed:
                #     already_printed.add((from_cell, from_direction))
                #     should_print = True

            # Check if wall
            if grid[row + dr][col + dc] == '#':
                break

            row += dr
            col += dc
            if new_direction is not None:
                direction = new_direction
            output_grid[row][col] = ['>', 'v', '<', '^'][direction]

    if should_print:
        print(instruction)
        print(*(''.join(l) for l in output_grid), sep='\n')
        print()
        sys.exit(0)

# Compute password
print(row, col, direction)
print(1000 * row + 4 * col + direction)
