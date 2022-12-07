import sys

SCORES = {
    'X': 0,
    'Y': 3,
    'Z': 6,
    'A': 1,
    'B': 2,
    'C': 3
}
WINNERS = {
    'A': 'CAB',
    'B': 'ABC',
    'C': 'BCA'
}

score = 0

for line in sys.stdin:
    a, b = line.split()

    score += SCORES[b]
    score += SCORES[WINNERS[a][SCORES[b] // 3]]

print(score)