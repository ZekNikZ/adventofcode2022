import sys
import queue
import time

grid = [[int(x) for x in line.strip()] for line in sys.stdin.readlines()]
num_rows = len(grid)
num_cols = len(grid[0])
best_so_far = 0

def print_grid(g):
    for row in g:
        print(' '.join(str(x) if x != -1 else '.' for x in row))

for row in range(1, num_rows - 1):
    for col in range(1, num_cols - 1):
        # Up
        r = row - 1
        up_count = 1
        while r > 0 and grid[r][col] < grid[row][col]:
            r -= 1
            up_count += 1

        # Down
        r = row + 1
        down_count = 1
        while r < num_rows - 1 and grid[r][col] < grid[row][col]:
            r += 1
            down_count += 1

        # Left
        c = col - 1
        left_count = 1
        while c > 0 and grid[row][c] < grid[row][col]:
            c -= 1
            left_count += 1

        # Right
        c = col + 1
        right_count = 1
        while c < num_cols - 1 and grid[row][c] < grid[row][col]:
            c += 1
            right_count += 1

        print(row, col, left_count, right_count, up_count, down_count)
        score = left_count * right_count * up_count * down_count

        best_so_far = max(best_so_far, score)

print(best_so_far)