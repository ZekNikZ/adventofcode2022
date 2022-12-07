s = input()

# Puzzle 1
for i in range(len(s) - 3):
    x = s[i:i+4]
    if len(set(x)) == 4:
        print(i+4)
        break

# Puzzle 2
for i in range(len(s) - 13):
    x = s[i:i+14]
    if len(set(x)) == 14:
        print(i+14)
        break