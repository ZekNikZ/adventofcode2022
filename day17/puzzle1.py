def print_chamber(chamber: list[list[bool]]):
    for row in reversed(chamber):
        print(*('#' if x else '.' for x in row), sep='')
    print()


class Rock:
    width: int
    height: int
    shape: list[list[bool]]

    def __init__(self, width: int, height: int, shape: list[list[bool]]):
        self.width = width
        self.height = height
        self.shape = shape

    def can_place_at(self, chamber: list[list[bool]], x: int, y: int) -> bool:
        if x < 0 or (x + self.width - 1) >= 7:
            return False

        if y < 0:
            return False

        for xx in range(x, x + self.width):
            for yy in range(y, y + self.height):
                if self.shape[yy - y][xx - x] and chamber[yy][xx]:
                    return False

        return True

    def place_at(self, chamber: list[list[bool]], x: int, y: int):
        for xx in range(x, x + self.width):
            for yy in range(y, y + self.height):
                if self.shape[yy - y][xx - x]:
                    chamber[yy][xx] = True


rocks = [
    Rock(4, 1, [[True, True, True, True]]),
    Rock(3, 3, [[False, True, False], [
         True, True, True], [False, True, False]]),
    Rock(3, 3, [[True, True, True], [
         False, False, True], [False, False, True]]),
    Rock(1, 4, [[True], [True], [True], [True]]),
    Rock(2, 2, [[True, True], [True, True]])
]

directions = input()
direction_counter = 0

max_height = 0
chamber = []
for rock_counter in range(2022):
    rock = rocks[rock_counter % len(rocks)]
    while len(chamber) < max_height + 3 + rock.height:
        chamber.append([False] * 7)

    x = 2
    y = max_height + 3
    # print('S', x, y)
    while True:
        # Move over
        direction = 1 if directions[direction_counter %
                                    len(directions)] == ">" else -1
        direction_counter += 1
        if rock.can_place_at(chamber, x + direction, y):
            x += direction
        # print('<' if direction == -1 else '>', x, y)

        # Move down
        if rock.can_place_at(chamber, x, y - 1):
            y -= 1
        else:
            rock.place_at(chamber, x, y)
            max_height = max(max_height, y + rock.height)
            break
        # print('v', x, y)

    # print_chamber(chamber)
    # print("=======")
    # print()

print(max_height)
