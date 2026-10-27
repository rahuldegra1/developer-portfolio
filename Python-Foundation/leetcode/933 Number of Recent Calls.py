from collections import deque


class RecentCounter:
    def __init__(self):

        self.queue = deque()

    def ping(self, t):

        self.queue.append(t)

        while self.queue and self.queue[0] < t - 3000:
            self.queue.popleft()

        return len(self.queue)


if __name__ == "__main__":
    counter = RecentCounter()

    print(f"Ping at 1ms. Recent calls: {counter.ping(1)}")  # Should be 1
    print(f"Ping at 100ms. Recent calls: {counter.ping(100)}")  # Should be 2
    print(f"Ping at 3001ms. Recent calls: {counter.ping(3001)}")  # Should be 3
    print(
        f"Ping at 3002ms. Recent calls: {counter.ping(3002)}"
    )  # Should be 3 (The 1ms ping expired!)
