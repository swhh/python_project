from sys import argv
import heapq


def bigger(list_a, list_b):
    diff = abs(len(list_a) - len(list_b))
    if len(list_b) > len(list_a):
        return diff, list_b
    return diff, list_a


class MedianMaintenance(object):

    def __init__(self):
        self.heap_low = []
        self.heap_high = []

    def compute_median(self):
        __, larger = bigger(self.heap_low, self.heap_high)
        return larger[0] if larger == self.heap_high else -larger[0]

    def add_element(self, element):
        if len(self.heap_high) > 0 and self.heap_high[0] <= element:
            heapq.heappush(self.heap_high, element)
        else:
            heapq.heappush(self.heap_low, -element)

        diff, larger = bigger(self.heap_low, self.heap_high)
        if diff > 1:
            moved = heapq.heappop(larger)
            if larger == self.heap_low:
                heapq.heappush(self.heap_high, -moved)
            else:
                heapq.heappush(self.heap_low, -moved)


if __name__ == '__main__':
    f = argv[1]
    median_tracker = MedianMaintenance()
    total = 0
    with open(f) as f:
        for line in f:
            median_tracker.add_element(int(line))
            total += median_tracker.compute_median()
    print total % 10000



