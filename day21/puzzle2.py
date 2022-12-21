import sys
from collections import defaultdict


class MyVal:
    operations: list[tuple[str, int]]

    def __init__(self):
        self.operations = []

    def __add__(self, other: int):
        self.operations.append(('add', other))
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        self.operations.append(('mul', other))
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        self.operations.append(('sub', other))
        return self

    def __rsub__(self, other):
        self.operations.append(('rsub', other))
        return self

    def __truediv__(self, other):
        self.operations.append(('div', other))
        return self

    def __rtruediv__(self, other):
        self.operations.append(('rdiv', other))
        return self

    def __str__(self):
        return f'MyVal({self.operations})'

    def __iter__(self):
        yield from reversed(self.operations)


print(2 / MyVal() / 3)


OPERATIONS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b
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
    elif name == "humn":
        monkeys[name] = ('constant', MyVal())
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

sorted_monkeys.remove("root")
sorted_monkeys.append("root")

monkey_values = {}
# do everything except root, since we'll handle that separately
for monkey_name in sorted_monkeys[:-1]:
    op, *args = monkeys[monkey_name]
    if op == 'constant':
        monkey_values[monkey_name] = args[0]
    else:
        a = monkey_values[args[0]]
        b = monkey_values[args[1]]
        monkey_values[monkey_name] = OPERATIONS[op](a, b)

_, a, b = monkeys["root"]
val, res = monkey_values[a], monkey_values[b]
if type(res) is MyVal:
    val, res = res, val

# print(val, res)

for op, arg in val:
    match op:
        case 'add':
            res -= arg
        case 'mul':
            res //= arg
        case 'sub':
            res += arg
        case 'div':
            res *= arg
        case 'rsub':
            res = arg - res
        case 'rdiv':
            res = arg // res

print(res)
