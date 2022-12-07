import sys
import string

PRIORITIES = ' ' + string.ascii_lowercase + string.ascii_uppercase

res = 0
for line in sys.stdin:
    s = line.strip()
    first_half, second_half = s[:len(s)//2], s[len(s)//2:]
    for c in set(first_half) & set(second_half):
        res += PRIORITIES.index(c)

print(res)