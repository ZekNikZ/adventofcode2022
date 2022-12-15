import sys

total = 0
for line in sys.stdin:
    x, y, z = map(int, line.strip().split('x'))

    # Wrapping outside
    total += 2 * min(x + y, y + z, z + x)

    # Bow
    total += x * y * z

print(total)
