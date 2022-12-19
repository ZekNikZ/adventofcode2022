import sys
from dataclasses import dataclass, asdict

# Optimizations:
#  1. Don't build another robot if we already have enough which generate the resources needed to build any other robot in one step
#  2. If we could build a geode robot in this step, don't bother trying to build other robots in this step


@dataclass()
class Blueprint:
    ore_robot_cost_ore: int
    clay_robot_cost_ore: int
    obsidian_robot_cost_ore: int
    obsidian_robot_cost_clay: int
    geode_robot_cost_ore: int
    geode_robot_cost_obsidian: int


@dataclass()
class State:
    blueprint: Blueprint

    ore_count: int = 0
    clay_count: int = 0
    obsidian_count: int = 0
    geode_count: int = 0

    ore_robot_count: int = 1
    clay_robot_count: int = 0
    obsidian_robot_count: int = 0
    geode_robot_count: int = 0

    mins_left: int = 24

    def clone(self):
        res = State(**asdict(self))
        res.blueprint = self.blueprint
        return res

    def next_minute(self):
        self.ore_count += self.ore_robot_count
        self.clay_count += self.clay_robot_count
        self.obsidian_count += self.obsidian_robot_count
        self.geode_count += self.geode_robot_count

        self.mins_left -= 1

        return self

    def can_buy_ore_robot(self):
        return self.ore_count >= self.blueprint.ore_robot_cost_ore and self.ore_robot_count < max(self.blueprint.ore_robot_cost_ore, self.blueprint.clay_robot_cost_ore, self.blueprint.obsidian_robot_cost_ore, self.blueprint.clay_robot_cost_ore)

    def buy_ore_robot(self):
        self.next_minute()

        self.ore_count -= self.blueprint.ore_robot_cost_ore
        self.ore_robot_count += 1

        return self

    def can_buy_clay_robot(self):
        return self.ore_count >= self.blueprint.clay_robot_cost_ore and self.clay_robot_count < self.blueprint.obsidian_robot_cost_clay

    def buy_clay_robot(self):
        self.next_minute()

        self.ore_count -= self.blueprint.clay_robot_cost_ore
        self.clay_robot_count += 1

        return self

    def can_buy_obsidian_robot(self):
        return self.ore_count >= self.blueprint.obsidian_robot_cost_ore and self.clay_count >= self.blueprint.obsidian_robot_cost_clay and self.obsidian_robot_count < self.blueprint.geode_robot_cost_obsidian

    def buy_obsidian_robot(self):
        self.next_minute()

        self.ore_count -= self.blueprint.obsidian_robot_cost_ore
        self.clay_count -= self.blueprint.obsidian_robot_cost_clay
        self.obsidian_robot_count += 1

        return self

    def can_buy_geode_robot(self):
        return self.ore_count >= self.blueprint.geode_robot_cost_ore and self.clay_count >= self.blueprint.geode_robot_cost_obsidian

    def buy_geode_robot(self):
        self.next_minute()

        self.ore_count -= self.blueprint.geode_robot_cost_ore
        self.obsidian_count -= self.blueprint.geode_robot_cost_obsidian
        self.geode_robot_count += 1

        return self


# Read blueprints
blueprints: list[Blueprint] = []
for line in sys.stdin:
    res = [int(i) for i in line.split() if i.isdigit()]
    blueprints.append(Blueprint(*res))


def compute(state: State):
    if state.mins_left == 0:
        return state.geode_count

    options = []
    bought_good_robot = False

    # Buy geode robot
    if state.can_buy_geode_robot():
        options.append(compute(state.clone().buy_geode_robot()))
        bought_good_robot = True

    # Buy obsidian robot
    if not bought_good_robot and state.can_buy_obsidian_robot():
        options.append(compute(state.clone().buy_obsidian_robot()))
        bought_good_robot = True

    # Buy ore robot
    if not bought_good_robot and state.can_buy_ore_robot():
        options.append(compute(state.clone().buy_ore_robot()))

    # Buy clay robot
    if not bought_good_robot and state.can_buy_clay_robot():
        options.append(compute(state.clone().buy_clay_robot()))

    options.append(compute(state.clone().next_minute()))

    return max(options)


options = []
for blueprint in blueprints:
    options.append(compute(State(blueprint)))

print(max(options))
