import sys

instructions = [line.strip() for line in sys.stdin]
IP = 0

X = 1
cycle_num = 1
current_instruction = ["noop", [], 1]

def noop():
    pass

def addx(a):
    global X
    X += int(a)

CYCLES_PER_INSTRUCTION = {
    "noop": 1,
    "addx": 2
}

INSTRUCTION_FUNCTIONS = {
    "noop": noop,
    "addx": addx
}

signal_strengths = []

while IP < len(instructions):
    if current_instruction[-1] == 1:
        # Apply current instruction
        INSTRUCTION_FUNCTIONS[current_instruction[0]](*current_instruction[1])

        # Fetch new instruction
        instruction, *args = instructions[IP].split()
        current_instruction = [instruction, args, CYCLES_PER_INSTRUCTION[instruction]]
        IP += 1
    else:
        current_instruction[-1] -= 1

    if (cycle_num + 20) % 40 == 0:
        signal_strengths.append(cycle_num * X)

    cycle_num += 1

print(signal_strengths)
print(sum(signal_strengths))