class Solution(object):
    def maxArea(self, height):
        res = []
        l, r = 0, len(height) - 1

        while l < r:
            area = (r - l) * min(height[l], height[r])
            res = self.maxArea(res)

            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return res
