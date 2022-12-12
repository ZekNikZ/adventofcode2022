import sys

input_grid = [[int(x) for x in line.strip()] for line in sys.stdin.readlines()]

def check_visibility_vertical(grid):
    res = set()

    max_heights = [-1] * len(grid[0])

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] > max_heights[col]:
                max_heights[col] = grid[row][col]
                res.add((row, col))

    return res

def check_visibility_horizontal(grid):
    res = set()

    max_heights = [-1] * len(grid)

    for col in range(len(grid[0])):
        for row in range(len(grid)):
            if grid[row][col] > max_heights[row]:
                max_heights[row] = grid[row][col]
                res.add((row, col))

    return res

res = set()

# Normal orientation
normal = check_visibility_vertical(input_grid)
res.update(normal)

# Vertical flip
vertical = check_visibility_vertical(input_grid[::-1])
res.update((len(input_grid) - 1 - row, col) for row, col in vertical)

# Left
left = check_visibility_horizontal(input_grid)
res.update(left)

# Right
right = check_visibility_horizontal(input_grid)
res.update((row, len(input_grid[0]) - 1 - col) for row, col in right)

print(res)
print(len(res))