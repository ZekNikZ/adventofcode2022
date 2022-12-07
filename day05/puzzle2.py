import sys

# parse stacks
input_lines = []
for line in sys.stdin:
    if len(line.strip()) == 0:
        break

    input_lines.append(line[1::4])

input_lines.pop() # remove line with numbers

stacks = [[y for y in x[::-1] if y != ' '] for x in zip(*input_lines)]

for line in sys.stdin:
    num_to_move, start, end = map(int, line.split()[1::2])
    boxes_to_move = stacks[start - 1][-num_to_move:]
    stacks[start - 1] = stacks[start - 1][:-num_to_move]
    stacks[end - 1] += boxes_to_move

print(''.join(x[-1] for x in stacks))