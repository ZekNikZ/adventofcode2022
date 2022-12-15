import sys

target_y = 2000000

sensors = []
beacons = set()

for line in sys.stdin:
    parts = line.strip().replace('=', '@').replace(',',
                                                   '@').replace('.', '@').replace(':', '@').split('@')
    # print(parts)
    x1, y1, x2, y2 = map(int, (parts[1], parts[3], parts[-3], parts[-1]))
    # print(x1, y1, x2, y2)

    dist = abs(x1 - x2) + abs(y1 - y2)

    sensors.append((x1, y1, dist))
    if y2 == target_y:
        beacons.add(x2)

print(sensors)

res = set()

for sx, y, d in sensors:
    delta = d - abs(y - target_y)
    for x in range(sx - delta, sx + delta + 1):
        res.add(x)

res -= beacons

# print(res)
print(len(res))
