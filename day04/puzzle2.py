import sys

ranges = [tuple(tuple(map(int, x.split('-'))) for x in line.strip().split(',')) for line in sys.stdin]
# print(ranges)

count = 0
for (x1, x2), (y1, y2) in ranges:
    a = set(range(x1, x2 + 1))
    b = set(range(y1, y2 + 1))
    if len(a | b) < len(a) + len(b):
        count += 1

print(count)