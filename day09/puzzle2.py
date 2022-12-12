import sys

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0

res = set()

NUM_KNOTS = 10
knots = [[0, 0] for _ in range(NUM_KNOTS)]

for line in sys.stdin:
    direction, steps = line.split()
    steps = int(steps)

    for _ in range(steps):
        # Adjust head
        if direction == 'U':
            knots[0][1] += 1
        elif direction == 'D':
            knots[0][1] -= 1
        elif direction == 'L':
            knots[0][0] -= 1
        elif direction == 'R':
            knots[0][0] += 1

        for i in range(1, NUM_KNOTS):
            head = knots[i - 1]
            tail = knots[i]

            # Adjust tail
            delta_x = head[0] - tail[0]
            delta_y = head[1] - tail[1]
            if abs(delta_x) > 1 and delta_y != 0:
                tail[0] += sign(delta_x)
                tail[1] += sign(delta_y)
            elif abs(delta_y) > 1 and delta_x != 0:
                tail[0] += sign(delta_x)
                tail[1] += sign(delta_y)
            elif abs(delta_x) > 1:
                tail[0] += sign(delta_x)
            elif abs(delta_y) > 1 :
                tail[1] += sign(delta_y)

        print(direction, knots)

        # Record tail position
        res.add((knots[-1][0], knots[-1][1]))

print(len(res))