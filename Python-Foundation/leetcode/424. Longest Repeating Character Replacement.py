class Solution:

  def characterReplacement(self, s: str, k: int) -> int:
    counts: dict[str, int] = {}
    left = 0
    max_freq = 0

    for right, char in enumerate(s):
      counts[char] = counts.get(char, 0) + 1
      if counts[char] > max_freq:
        max_freq = counts[char]

      # If invalid, shift the window forward by 1 (size stays constant)
      if (right - left + 1) - max_freq > k:
        counts[s[left]] -= 1
        left += 1

    # The maximum window length reached is preserved until the end
    return len(s) - left 