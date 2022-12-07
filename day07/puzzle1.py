import sys
import pprint

class node:
    parent: 'node'
    name: str
    is_dir: bool
    children: dict[str,'node']
    size: int

    def __init__(self, parent: 'node', name: str, is_dir: bool, size: int=-1) -> None:
        self.parent = parent
        self.name = name
        self.is_dir = is_dir
        self.children = {}
        self.size = size

    def dict(self):
        res = {}

        for k, v in self.children.items():
            if v.is_dir:
                res[k] = v.dict()
            else:
                res[k] = v.size

        return res

    def compute_size(self):
        if not self.is_dir:
            return

        for v in self.children.values():
            v.compute_size()

        self.size = sum(v.size for v in self.children.values())

    def __repr__(self) -> str:
        return f'node(name={self.name}, parent={self.parent.name if self.parent is not None else "None"})'

lines = [x.strip() for x in sys.stdin.readlines()]

tree = node(None, '/', True)
current_dir = tree

i = 0
while i < len(lines):
    # print(current_dir, end=' ')
    command = lines[i][2: ]
    # print(command)
    if command.startswith('cd'):
        new_dir = command.split()[1]
        if new_dir == '/':
            current_dir = tree
        elif new_dir == '..':
            current_dir = current_dir.parent
        else:
            current_dir = current_dir.children[new_dir]
        i += 1
        continue
    else:
        i += 1
        while i < len(lines) and not lines[i].startswith('$'):
            a, b = lines[i].split()
            if a == 'dir':
                if b not in current_dir.children.keys():
                    current_dir.children[b] = node(current_dir, b, True)
                # print(f'  created dir {current_dir.children[b]}')
            else:
                if a not in current_dir.children.keys():
                    current_dir.children[b] = node(current_dir, b, False, int(a))
                # print(f'  created file {current_dir.children[b]}')
            i += 1

# Compute sizes
tree.compute_size()

# List directories
dirs = []
def list_directories(node: node):
    if node.is_dir:
        dirs.append(node)
        for v in node.children.values():
            list_directories(v)

list_directories(tree)
print(sum(x.size for x in dirs if x.size <= 100000))