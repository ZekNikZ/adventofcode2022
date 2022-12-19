import sys

data = set(tuple(map(int, line.strip().split(',')))
           for line in sys.stdin.readlines())

total = 0
for point in data:
    x, y, z = point
    if (x - 1, y, z) not in data:
        total += 1
    if (x + 1, y, z) not in data:
        total += 1
    if (x, y - 1, z) not in data:
        total += 1
    if (x, y + 1, z) not in data:
        total += 1
    if (x, y, z - 1) not in data:
        total += 1
    if (x, y, z + 1) not in data:
        total += 1

print(total)
