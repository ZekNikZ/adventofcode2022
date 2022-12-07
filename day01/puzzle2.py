import sys

elves = []

current = 0
for line in sys.stdin:
    num = int(line) if line.strip().isdecimal() else None

    if num is None:
        elves.append(current)
        current = 0
    else:
        current += num

if current > 0:
    elves.append(current)

nums = list(sorted(elves, reverse=True))
print(sum(nums[:3]))
