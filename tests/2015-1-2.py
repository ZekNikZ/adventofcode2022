s = input()

c = 0
for i in range(len(s)):
    if s[i] == '(':
        c += 1
    else:
        c -= 1

    if c < 0:
        print(i + 1)
        break
