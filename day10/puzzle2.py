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

    if abs(((cycle_num-1) % 40) - X) <= 1:
        print("#", end="")
    else:
        print(".", end="")

    if cycle_num % 40 == 0:
        print()

    cycle_num += 1