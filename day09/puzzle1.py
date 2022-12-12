import sys

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0

res = set()

head_x = 0
head_y = 0
tail_x = 0
tail_y = 0

for line in sys.stdin:
    direction, steps = line.split()
    steps = int(steps)

    for _ in range(steps):
        # Adjust head
        if direction == 'U':
            head_y += 1
        elif direction == 'D':
            head_y -= 1
        elif direction == 'L':
            head_x -= 1
        elif direction == 'R':
            head_x += 1

        # Adjust tail
        delta_x = head_x - tail_x
        delta_y = head_y - tail_y
        if abs(delta_x) > 1 and delta_y != 0:
            tail_x += sign(delta_x)
            tail_y = head_y
        elif abs(delta_y) > 1 and delta_x != 0:
            tail_x = head_x
            tail_y += sign(delta_y)
        elif abs(delta_x) > 1:
            tail_x += sign(delta_x)
        elif abs(delta_y) > 1 :
            tail_y += sign(delta_y)

        print(direction, head_x, head_y, tail_x, tail_y)

        # Record tail position
        res.add((tail_x, tail_y))

print(len(res))