import sys

nums = list(enumerate(int(x) for x in sys.stdin))

# print(nums)
# print()

for i in range(len(nums)):
    old_index, t = next(filter(lambda e: e[1][0] == i, enumerate(nums)))
    i, num = t

    new_index = (old_index + num) % (len(nums) - 1)

    if old_index < new_index:
        nums[old_index:new_index] = nums[old_index + 1:new_index + 1]
    elif old_index > new_index:
        nums[new_index + 1:old_index + 1] = nums[new_index:old_index]
    nums[new_index] = t

    # print(num, old_index, "->", new_index, nums)
    # print()

i = next(i for i, e in enumerate(nums) if e[1] == 0)
print(sum(nums[(i + x) % len(nums)][1] for x in range(1000, 3001, 1000)))
