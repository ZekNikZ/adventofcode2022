import sys

lines = map(str.strip, sys.stdin.readlines())

grid = set()
max_y = -1

for line in lines:
    sections = [tuple(map(int, x.split(','))) for x in line.split(' -> ')]
    pairs = list(zip(sections, sections[1:]))

    for first, second in pairs:
        x1, y1 = first
        x2, y2 = second

        max_y = max(max_y, y1, y2)

        if x1 == x2:
            # Horizontal
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid.add((x1, y))
        else:
            # Vertical
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid.add((x, y1))


count = 0
while True:
    x, y = 500, 0

    flag = False

    while True:
        print(x, y, count)
        if y >= max_y:
            flag = True
            break

        if (x, y + 1) not in grid:
            y += 1
        elif (x - 1, y + 1) not in grid:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in grid:
            x += 1
            y += 1
        else:
            grid.add((x, y))
            break

    if flag:
        break
    count += 1

print(count)
