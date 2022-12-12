NUM_ROUNDS = 20

def add(n):
    return lambda x: x + n

def multiply(n):
    return lambda x: x * n

def square(x):
    return x * x

monkeys = []

while True:
    try:
        if len(monkeys) > 0:
            input()
        input()
        _, starting_items_raw = input().split(": ")
        starting_items = list(map(int, starting_items_raw.split(", ")))
        _, _, _, var1, op, var2 = input().split()
        test_num = int(input().split()[-1])
        if_true = int(input().split()[-1])
        if_false = int(input().split()[-1])

        operation = None
        if op == '+':
            operation = add(int(var2))
        elif op == '*':
            if var2 == "old":
                operation = square
            else:
                operation = multiply(int(var2))
    except EOFError:
        break

    monkeys.append({
        "inventory": starting_items,
        "operation": operation,
        "test": test_num,
        "next": [if_false, if_true]
    })

inspection_counts = [0] * len(monkeys)
for _ in range(NUM_ROUNDS):
    for i, monkey in enumerate(monkeys):
        for item in monkey["inventory"]:
            inspection_counts[i] += 1
            new_item = monkey["operation"](item) // 3
            monkeys[monkey["next"][int(new_item % monkey["test"] == 0)]]["inventory"].append(new_item)
        monkey["inventory"] = []

    for monkey in monkeys:
        print(monkey["inventory"])
    print("----")

print(inspection_counts)
s = sorted(inspection_counts)
print(s[-1] * s[-2])