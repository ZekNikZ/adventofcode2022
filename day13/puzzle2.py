import functools

packets = [
    [[2]],
    [[6]]
]


def compare(a, b):
    if isinstance(a, list) and not isinstance(b, list):
        return compare(a, [b])
    elif not isinstance(a, list) and isinstance(b, list):
        return compare([a], b)
    elif isinstance(a, int) and isinstance(b, int):
        return b - a
    else:
        for i in range(min(len(a), len(b))):
            x = compare(a[i], b[i])
            if x < 0:
                return -1
            elif x > 0:
                return 1
        else:
            return len(b) - len(a)


while True:
    try:
        i = input()
        if len(i) > 0:
            x = eval(i)
            packets.append(x)
    except EOFError:
        break

packets.sort(key=functools.cmp_to_key(compare), reverse=True)
print((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))
