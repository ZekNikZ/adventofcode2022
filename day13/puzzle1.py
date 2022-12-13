pairs = []


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


total = 0
while True:
    try:
        if len(pairs) > 0:
            input()
        a = eval(input())
        b = eval(input())
        pairs.append((a, b))

        x = compare(a, b)
        print(a, b)
        print(x)
        print()

        if x > 0:
            total += len(pairs)
    except EOFError:
        break

print(total)
