import sys


def convert_to_snafu(num: int):
    res = ''
    while num != 0:
        num, m = divmod(num, 5)
        if m >= 3:
            num += 1
            m -= 5
        res += "=-012"[m+2]
    return res[::-1]


def convert_to_decimal(num: str):
    res = 0
    for c in num:
        res *= 5
        res += [-2, -1, 0, 1, 2]["=-012".index(c)]
    return res


print(convert_to_snafu(sum(convert_to_decimal(l.strip()) for l in sys.stdin)))
