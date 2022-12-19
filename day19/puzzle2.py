import sys
from dataclasses import dataclass, asdict
from math import *

# Optimizations:
#  1. Don't build another robot if we already have enough which generate the resources needed to build any other robot in one step
#  2. Don't simulate minute-by-minute, only simulate choosing which robot to buy next and waiting until we have the resources to build that robot
#  3. Prune tracks that can never beat the best so far (i.e., if we would produce geode robots on every turn starting now (regardless of whether or not this is possible), could we beat the best so far?)


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

    mins_left: int = 32

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

    def skip_to_end(self):
        self.ore_count += self.ore_robot_count * self.mins_left
        self.clay_count += self.clay_robot_count * self.mins_left
        self.obsidian_count += self.obsidian_robot_count * self.mins_left
        self.geode_count += self.geode_robot_count * self.mins_left

        return self

    def can_buy_ore_robot(self):
        enough_time_left = self.blueprint.ore_robot_cost_ore - self.ore_count <= (
            self.mins_left - 1) * self.ore_robot_count
        return enough_time_left and self.ore_robot_count < max(self.blueprint.ore_robot_cost_ore, self.blueprint.clay_robot_cost_ore, self.blueprint.obsidian_robot_cost_ore, self.blueprint.clay_robot_cost_ore)

    def buy_ore_robot(self):
        mins_needed = max(0, ceil(
            (self.blueprint.ore_robot_cost_ore - self.ore_count) / self.ore_robot_count)) + 1
        self.ore_count += mins_needed * self.ore_robot_count
        self.clay_count += mins_needed * self.clay_robot_count
        self.obsidian_count += mins_needed * self.obsidian_robot_count
        self.geode_count += mins_needed * self.geode_robot_count

        self.ore_count -= self.blueprint.ore_robot_cost_ore
        self.ore_robot_count += 1

        self.mins_left -= mins_needed

        return self

    def can_buy_clay_robot(self):
        enough_time_left = self.blueprint.clay_robot_cost_ore - self.ore_count <= (
            self.mins_left - 1) * self.ore_robot_count
        return enough_time_left and self.clay_robot_count < self.blueprint.obsidian_robot_cost_clay

    def buy_clay_robot(self):
        mins_needed = max(0, ceil(
            (self.blueprint.clay_robot_cost_ore - self.ore_count) / self.ore_robot_count)) + 1
        self.ore_count += mins_needed * self.ore_robot_count
        self.clay_count += mins_needed * self.clay_robot_count
        self.obsidian_count += mins_needed * self.obsidian_robot_count
        self.geode_count += mins_needed * self.geode_robot_count

        self.ore_count -= self.blueprint.clay_robot_cost_ore
        self.clay_robot_count += 1

        self.mins_left -= mins_needed

        return self

    def can_buy_obsidian_robot(self):
        enough_time_left = self.blueprint.obsidian_robot_cost_ore - self.ore_count <= (
            self.mins_left - 1) * self.ore_robot_count and self.blueprint.obsidian_robot_cost_clay - self.clay_count <= (self.mins_left - 1) * self.clay_robot_count
        return enough_time_left and self.obsidian_robot_count < self.blueprint.geode_robot_cost_obsidian

    def buy_obsidian_robot(self):
        mins_needed = max(0, ceil(
            (self.blueprint.obsidian_robot_cost_ore - self.ore_count) / self.ore_robot_count), ceil(
            (self.blueprint.obsidian_robot_cost_clay - self.clay_count) / self.clay_robot_count)) + 1
        self.ore_count += mins_needed * self.ore_robot_count
        self.clay_count += mins_needed * self.clay_robot_count
        self.obsidian_count += mins_needed * self.obsidian_robot_count
        self.geode_count += mins_needed * self.geode_robot_count

        self.ore_count -= self.blueprint.obsidian_robot_cost_ore
        self.clay_count -= self.blueprint.obsidian_robot_cost_clay
        self.obsidian_robot_count += 1

        self.mins_left -= mins_needed

        return self

    def can_buy_geode_robot(self):
        enough_time_left = self.blueprint.geode_robot_cost_ore - self.ore_count <= (
            self.mins_left - 1) * self.ore_robot_count and self.blueprint.geode_robot_cost_obsidian - self.obsidian_count <= (self.mins_left - 1) * self.obsidian_robot_count
        return enough_time_left

    def buy_geode_robot(self):
        mins_needed = max(0, ceil(
            (self.blueprint.geode_robot_cost_ore - self.ore_count) / self.ore_robot_count), ceil(
            (self.blueprint.geode_robot_cost_obsidian - self.obsidian_count) / self.obsidian_robot_count)) + 1
        self.ore_count += mins_needed * self.ore_robot_count
        self.clay_count += mins_needed * self.clay_robot_count
        self.obsidian_count += mins_needed * self.obsidian_robot_count
        self.geode_count += mins_needed * self.geode_robot_count

        self.ore_count -= self.blueprint.geode_robot_cost_ore
        self.obsidian_count -= self.blueprint.geode_robot_cost_obsidian
        self.geode_robot_count += 1

        self.mins_left -= mins_needed

        return self


# Read blueprints
blueprints: list[Blueprint] = []
for line in sys.stdin:
    res = [int(i) for i in line.split() if i.isdigit()]
    blueprints.append(Blueprint(*res))


best_so_far = 0


def compute(state: State):
    global best_so_far

    if state.geode_count + state.mins_left * (state.geode_robot_count - 1) + (state.mins_left * state.mins_left + 1) // 2 < best_so_far:
        return 0

    if state.mins_left <= 0:
        if state.geode_count > best_so_far:
            best_so_far = state.geode_count
        return state.geode_count

    options = []
    bought_any_robot = False

    # Try buying geode robot next
    if state.can_buy_geode_robot():
        options.append(compute(state.clone().buy_geode_robot()))
        bought_any_robot = True

    # Try buying obsidian robot next
    if state.can_buy_obsidian_robot():
        options.append(compute(state.clone().buy_obsidian_robot()))
        bought_any_robot = True

    # Try buying clay robot next
    if state.can_buy_clay_robot():
        options.append(compute(state.clone().buy_clay_robot()))
        bought_any_robot = True

    # Try buying ore robot next
    if state.can_buy_ore_robot():
        options.append(compute(state.clone().buy_ore_robot()))
        bought_any_robot = True

    if not bought_any_robot:
        res = state.clone().skip_to_end().geode_count
        if res > best_so_far:
            best_so_far = res
        return res

    return max(options)


total = 1
for blueprint in blueprints[:3]:
    best_so_far = 0
    total *= compute(State(blueprint))

print(total)
