class Solution(object):
    def twoSum(self, nums, target):
        history = {}
        for index, num in enumerate(nums):
            needed = target - num
            if needed in history:
                return [history[needed], index]
            history[num] = index
