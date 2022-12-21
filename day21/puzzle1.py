import sys
from collections import defaultdict

OPERATIONS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b
}

monkeys = {}
dependencies = defaultdict(set)

for line in sys.stdin:
    name, *rest = line.strip().split()
    name = name[:-1]  # remove colon
    if len(rest) == 3:
        a, op, b = rest
        monkeys[name] = (op, a, b)
        dependencies[a].add(name)
        dependencies[b].add(name)
    else:
        monkeys[name] = ('constant', int(rest[0]))

# Topological sort
sorted_monkeys = []
visited = set()


def visit(monkey_name, v: set[str]):
    if monkey_name in visited:
        return
    if monkey_name in v:
        print("ERROR")
        sys.exit(1)

    v.add(monkey_name)

    for dependent in dependencies[monkey_name]:
        visit(dependent, v)

    v.remove(monkey_name)
    visited.add(monkey_name)
    sorted_monkeys.insert(0, monkey_name)


for monkey_name in monkeys.keys():
    if monkey_name not in visited:
        visit(monkey_name, set())

monkey_values = {}
for monkey_name in sorted_monkeys:
    op, *args = monkeys[monkey_name]
    if op == 'constant':
        monkey_values[monkey_name] = args[0]
    else:
        monkey_values[monkey_name] = OPERATIONS[op](
            monkey_values[args[0]], monkey_values[args[1]])

print(monkey_values["root"])
