import sys

ranges = [tuple(tuple(map(int, x.split('-'))) for x in line.strip().split(',')) for line in sys.stdin]
# print(ranges)

count = 0
for (x1, x2), (y1, y2) in ranges:
    if x1 > y1: # x is (potentially) smaller
        if x2 <= y2:
            count += 1
    elif y1 > x1: # y is (potentially) smaller
        if y2 <= x2:
            count += 1
    elif x1 == y1: # same start
        count += 1
    elif x2 == y2:
        count += 1

print(count)