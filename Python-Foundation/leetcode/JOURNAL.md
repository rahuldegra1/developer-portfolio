# Problem Journal

A running log of what I tried and what actually clicked for each problem — written honestly, including the ones where I needed more help than others.

---

### 001 — Two Sum
- **Tried:** Took over an hour on my first attempt — had to actually understand how `class`/`def` work together and what `self` does, not just copy the shape.
- **Learned:** Got introduced to time complexity — realized a working solution isn't automatically a *good* one, and started thinking about how to make code more efficient.

---

### 002 — Palindrome Number
- **Tried:** Reverse the number and compare it to the original — had to decide between converting to a string or reversing it mathematically using `% 10` and `// 10`.
- **Learned:** Negative numbers can never be palindromes because of the minus sign, so those get filtered out immediately without needing to check anything else.

---

### 003 — Contains Duplicate
- **Tried:** Needed more outside help on this one than the others — looked things up rather than working it out independently.
- **Learned:** A hash set lets you check "have I seen this before?" in O(1) time, with an early exit the moment a duplicate shows up — no need to scan the rest of the list.

---

### 004 — Valid Anagram
- **Tried:** First version crashed because `self` was in the function signature outside of the LeetCode class wrapper — needed help identifying that mismatch.
- **Learned:** Counting each string's letters into two dictionaries and comparing them directly (`count_s == count_t`) is enough to prove two strings are anagrams.

---

### 005 — Group Anagrams (Medium)
- **Tried:** My first Medium-level problem — needed a way to group words that are anagrams of each other using sorted letters as a key.
- **Learned:** `sorted()` returns a list, but dictionary keys must be hashable — lists aren't, so `"".join()` converts it into a string first, which is hashable and works as a key.

---

### 006 — Valid Palindrome
- **Tried:** Handling spaces, punctuation, and uppercase characters before checking the string.
- **Learned:** Using two pointers (one at the start, one at the end) and moving them inward simultaneously allows you to verify symmetry in a single O(n) pass without creating reverse copies of the string.

---

### 007 — Valid Parentheses
- **Tried:** Handled indentation bugs and learned the hard way about LeetCode's Python 2 vs Python 3 dropdown crashing modern f-strings. Achieved a 0ms runtime.
- **Learned:** A Stack is LIFO (Last-In, First-Out). By using `.append()` to push opening brackets and `.pop()` to evaluate closing brackets against a dictionary map, you can perfectly track the inner-most pairs.

---

### 008 — Number of Recent Calls
- **Tried:** Built a hit-counter to track events strictly within a rolling 3000ms window. Hit type-hinting syntax errors before switching to the proper Python 3 environment. Achieved a 40ms runtime.
- **Learned:** A Queue is FIFO (First-In, First-Out). Using `collections.deque` allows for fast `.popleft()` operations to kick out the oldest data at the front without forcing Python to shift the entire list in memory.

---

### 009 — Two Sum II - Input Array Is Sorted
- **Tried:** Implemented pointers at the absolute minimum (left) and maximum (right) values, beating 81.61% of Python users on runtime.
- **Learned:** When an array is pre-sorted, using a Hash Map wastes memory. Placing pointers at opposite ends allows you to intuitively steer the sum directly to the target (drop the right if too high, raise the left if too low) in a single pass, operating in perfect O(1) space.

---

### 010 — Best Time to Buy and Sell Stock
- **Tried:** Hit a "Time Limit Exceeded" infinite loop because I put the right pointer increment inside the `else` block, and returned `null` by forgetting the variable in the return statement.
- **Learned:** The Sliding Window technique. Instead of checking every possible pair of days (O(n²)), use a left pointer for the buy day and a right pointer for the sell day. If you stumble across a price lower than your current buy price, instantly snap the left pointer to the right pointer's position. Keep pulling the right pointer forward to scan the rest of the array in O(n) time.

---

### 011 — Fibonacci Number
- **Tried:** Implemented pure, naive recursion. The runtime was slow (655 ms, beating only 22%), proving visually why exponential branching is dangerous.
- **Learned:** Every recursive function must have two things: a base case (the stop sign, like `if n == 0`) to prevent infinite loops, and a recursive step that calls a clone of itself (`self.fib(n - 1) + self.fib(n - 2)`). 

---

### Linear Algebra Fundamentals
- **Magnitude and Direction:** A vector always combines an amount or length (magnitude) with a specific pathway it points along (direction), unlike a scalar which is just a single numeric value.
- **Spatial Arrow vs. Data List:** A vector can be viewed geometrically as a directed arrow rooted in space or computer-scientifically as an ordered list of numbers representing coordinates.
- **Linear Operations:** A vector can be added to another vector or scaled (multiplied by a regular number) to change its length or reverse its direction while maintaining predictable geometric rules.