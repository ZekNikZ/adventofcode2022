import sys


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

output_grid = [list(l) for l in grid]

# Compute flipped grid
flipped_grid = list(''.join(l) for l in zip(*grid))

# Starting location
row: int = 1
col: int = grid[1].index('.')
direction: int = 0  # 0 = right, 1 = down, 2 = left, 3 = up

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
for instruction in instructions:
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
            if grid[row + dr][col + dc] == ' ':
                if dr == 1:
                    new_row = min(index(flipped_grid[col],
                                        '.'), index(flipped_grid[col], '#'))
                    dr = new_row - row
                elif dr == -1:
                    new_row = max(rindex(flipped_grid[col],
                                         '.'), rindex(flipped_grid[col], '#'))
                    dr = new_row - row
                elif dc == 1:
                    new_col = min(index(grid[row], '.'), index(grid[row], '#'))
                    dc = new_col - col
                else:
                    new_col = max(rindex(grid[row], '.'),
                                  rindex(grid[row], '#'))
                    dc = new_col - col

            # Check if wall
            if grid[row + dr][col + dc] == '#':
                break

            row += dr
            col += dc
            output_grid[row][col] = ['>', 'v', '<', '^'][direction]

    # print(instruction)
    # print(*(''.join(l) for l in output_grid), sep='\n')
    # print()

# Compute password
print(row, col, direction)
print(1000 * row + 4 * col + direction)
