import sys

total = 0
for line in sys.stdin:
    x, y, z = map(int, line.strip().split('x'))

    total += 2 * x * y + 2 * x * z + 2 * y * z + min(x * y, x * z, y * z)

print(total)
