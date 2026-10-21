class Solution:
    def findMin(self, nums):
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            # If mid element is greater than the right element,
            # the minimum must be in the right half
            if nums[mid] > nums[right]:
                left = mid + 1
            # Otherwise, the minimum is at mid or in the left half
            else:
                right = mid

        return nums[left]
