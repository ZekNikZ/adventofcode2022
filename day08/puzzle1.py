import sys
import queue
import time

grid = [[int(x) for x in line.strip()] for line in sys.stdin.readlines()]
num_rows = len(grid)
num_cols = len(grid[0])
res = set()
res_grid = None
SLEEP_TIME = 0.05

def print_grid(g):
    for row in g:
        print(' '.join(str(x) if x != -1 else '.' for x in row))

def setup():
    global res_grid
    res_grid = [[-1] * num_cols for _ in range(num_rows)]
    # Setup edges
    for row in range(num_rows):
        res_grid[row][0] = grid[row][0]
        res_grid[row][-1] = grid[row][-1]
        res.add((row, 0))
        res.add((row, num_cols - 1))

    for col in range(num_cols):
        res_grid[0][col] = grid[0][col]
        res_grid[-1][col] = grid[-1][col]
        res.add((0, col))
        res.add((num_rows - 1, col))

def top_to_bottom():
    setup()
    for row in range(1, num_rows - 1):
        for col in range(1, num_cols - 1):
            res_grid[row][col] = max(
                grid[row][col],
                res_grid[row - 1][col]
            )
            if grid[row][col] > res_grid[row - 1][col]:
                res.add((row, col))
        # print_grid(res_grid)
        # time.sleep(SLEEP_TIME)

def bottom_to_top():
    setup()
    for row in reversed(range(1, num_rows - 1)):
        for col in range(1, num_cols - 1):
            res_grid[row][col] = max(
                grid[row][col],
                res_grid[row + 1][col]
            )
            if grid[row][col] > res_grid[row + 1][col]:
                res.add((row, col))
        # print_grid(res_grid)
        # time.sleep(SLEEP_TIME)

def left_to_right():
    setup()
    for col in range(1, num_cols - 1):
        for row in range(1, num_rows - 1):
            res_grid[row][col] = max(
                grid[row][col],
                res_grid[row][col - 1]
            )
            if grid[row][col] > res_grid[row][col - 1]:
                res.add((row, col))
        # print_grid(res_grid)
        # time.sleep(SLEEP_TIME)

def right_to_left():
    setup()
    for col in reversed(range(1, num_cols - 1)):
        for row in range(1, num_rows - 1):
            res_grid[row][col] = max(
                grid[row][col],
                res_grid[row][col + 1]
            )
            if grid[row][col] > res_grid[row][col + 1]:
                res.add((row, col))
        # print_grid(res_grid)
        # time.sleep(SLEEP_TIME)

top_to_bottom()
bottom_to_top()
left_to_right()
right_to_left()

print(len(res))