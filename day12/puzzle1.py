import sys

grid = [list(line.strip()) for line in sys.stdin]

# find S
start = None
for i in range(len(grid)):
    if 'S' in grid[i]:
        start = (i, grid[i].index('S'))
        grid[start[0]][start[1]] = 'a'
        break

# find E
end = None
for i in range(len(grid)):
    if 'E' in grid[i]:
        end = (i, grid[i].index('E'))
        grid[end[0]][end[1]] = 'z'
        break

visited = [[False] * len(grid[0]) for _ in range(len(grid))]
dist = [[-1] * len(grid[0]) for _ in range(len(grid))]
q = [start]
dist[start[0]][start[1]] = 0


def is_adjacent(x, y):
    return ord(grid[y[0]][y[1]]) - ord(grid[x[0]][x[1]]) <= 1


def adjacent(row, col):
    if row > 0 and is_adjacent((row, col), (row - 1, col)):
        yield (row - 1, col)

    if col > 0 and is_adjacent((row, col), (row, col - 1)):
        yield (row, col - 1)

    if row < len(grid) - 1 and is_adjacent((row, col), (row + 1, col)):
        yield (row + 1, col)

    if col < len(grid[0]) - 1 and is_adjacent((row, col), (row, col + 1)):
        yield (row, col + 1)


while len(q) > 0:
    row, col = q.pop(0)

    if visited[row][col]:
        continue
    # print(row, col)

    visited[row][col] = True

    for vrow, vcol in adjacent(row, col):
        if visited[vrow][vcol]:
            continue
        # print(" ->", vrow, vcol)

        dist[vrow][vcol] = dist[row][col] + 1

        if end == (vrow, vcol):
            print(dist[vrow][vcol])
            q = []
            break
        else:
            q.append((vrow, vcol))
