def print_chamber(chamber: list[list[bool]]):
    for row in reversed(chamber):
        print(*('#' if x else '.' for x in row), sep='')
    print()


class Rock:
    width: int
    height: int
    shape: list[list[bool]]
    heights: list[int]

    def __init__(self, width: int, height: int, shape: list[list[bool]], heights: list[int]):
        self.width = width
        self.height = height
        self.shape = shape
        self.heights = heights

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
    Rock(4, 1, [[True, True, True, True]], [1, 1, 1, 1]),
    Rock(3, 3, [[False, True, False], [
         True, True, True], [False, True, False]], [1, 3, 1]),
    Rock(3, 3, [[True, True, True], [
         False, False, True], [False, False, True]], [1, 1, 3]),
    Rock(1, 4, [[True], [True], [True], [True]], [4]),
    Rock(2, 2, [[True, True], [True, True]], [2, 2])
]

directions = input()
direction_counter = 0

# max_height = 0
# chamber = []
# found_cycle = False
# possible_cycles = []
# num_rocks_to_simulate = 1_000_000_000_000
# for rock_counter in range(num_rocks_to_simulate):
#     if found_cycle:
#         break

#     rock = rocks[rock_counter % len(rocks)]
#     while len(chamber) < max_height + 3 + rock.height:
#         chamber.append([False] * 7)

#     x = 2
#     y = max_height + 3
#     while True:
#         # Move over
#         direction = 1 if directions[direction_counter %
#                                     len(directions)] == ">" else -1
#         direction_counter += 1
#         if rock.can_place_at(chamber, x + direction, y):
#             x += direction

#         # Move down
#         if rock.can_place_at(chamber, x, y - 1):
#             y -= 1
#         else:
#             rock.place_at(chamber, x, y)
#             max_height = max(max_height, y + rock.height)

#             # if not found_cycle:
#             if all(chamber[max_height - 1]):
#                 print(max_height, rock_counter)
#                 possible_cycles.append(max_height)
#             break


direction_counter = 0
max_height = 0
chamber = []
# found_cycle = False
# possible_cycles = []
cycle_count = 1735
cycle_start = 650
num_rocks_to_simulate = (1_000_000_000_000 - cycle_start) % cycle_count
# num_rocks_to_simulate = 1_000_000_000_000
max_height_delta = 2673*((1_000_000_000_000-cycle_start)//cycle_count)+962
for rock_counter in range(num_rocks_to_simulate):
    # if rock_counter % (len(rocks) * len(directions)) == 0:
    #     print(rock_counter, max_height)

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

            # if not found_cycle:
            if all(chamber[max_height - 1]):
                print(max_height, rock_counter)
                # possible_cycles.append(max_height)
            break
        # print('v', x, y)

    # print_chamber(chamber)
    # print("=======")
    # print()


print(max_height, max_height_delta, max_height + max_height_delta)


# Answer is 1540634005751
