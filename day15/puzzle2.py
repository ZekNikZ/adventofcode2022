import sys

bounds = 4000000

sensors = []

for line in sys.stdin:
    parts = line.strip().replace('=', '@').replace(',',
                                                   '@').replace('.', '@').replace(':', '@').split('@')
    # print(parts)
    x1, y1, x2, y2 = map(int, (parts[1], parts[3], parts[-3], parts[-1]))
    # print(x1, y1, x2, y2)

    dist = abs(x1 - x2) + abs(y1 - y2)

    sensors.append((x1, y1, dist))

print(sensors)

possibilities = []
for tx in range(bounds + 1):
    excluded_regions = []
    for sx, y, d in sensors:
        delta = d - abs(sx - tx)
        if delta >= 0:
            excluded_regions.append((y - delta, y + delta))
            # print(excluded_regions[-1], sx, y, d, delta)

    excluded_regions.sort()

    # print(tx, excluded_regions)

    # if excluded_regions[0][0] > 0:
    #     possibilities.append((tx, 0))
    # if excluded_regions[-1][1] < bounds:
    #     possibilities.append((tx, bounds))

    prev_max = 0
    for i in range(len(excluded_regions) - 1):
        s1, e1 = excluded_regions[i]
        s2, e2 = excluded_regions[i + 1]

        # print(' ', prev_max, s1, e1, s2, e2)

        prev_max = max(prev_max, e1)

        if s2 - prev_max >= 2:
            # print(" ", "YES", (tx, e1 + 1))
            possibilities.append((tx, e1 + 1))

print(possibilities)

px, py = possibilities[0]
print(px * bounds + py)
