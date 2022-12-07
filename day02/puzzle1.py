import sys

SCORES = {
    'X': 1,
    'Y': 2,
    'Z': 3,
    'AY': 6,
    'BX': 0,
    'BZ': 0,
    'CX': 6,
    'BZ': 6,
    'CY': 0,
    'AZ': 0,
    'AX': 3,
    'BY': 3,
    'CZ': 3
}

score = 0

for line in sys.stdin:
    a, b = line.split()

    score += SCORES[b]
    score += SCORES[a + b]

print(score)