import sys
import string

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

PRIORITIES = ' ' + string.ascii_lowercase + string.ascii_uppercase

lines = [set(x.strip()) for x in sys.stdin.readlines()]

res = 0
for a, b, c in divide_chunks(lines, 3):
    for d in a & b & c:
        res += PRIORITIES.index(d)

print(res)