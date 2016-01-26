import sys


def sort(l):
    return merge_sort(l, 0, len(l)-1)


def merge_sort(l, lo, hi):
    if lo >= hi:
        return [l[lo]], 0
    mid = lo + (hi - lo)/2
    p1, x = merge_sort(l, lo, mid)
    p2, y = merge_sort(l, mid+1, hi)
    p, z = merge(p1, p2)
    return p, x+y+z


def merge(l1, l2):
    merged = []
    i = 0
    j = 0
    inversions = 0
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            merged.append(l1[i])
            i += 1
        else:
            merged.append(l2[j])
            j += 1
            inversions += (len(l1) - i)
    if i >= len(l1):
        while j < len(l2):
            merged.append(l2[j])
            j += 1
    if j >= len(l2):
        while i < len(l1):
            merged.append(l1[i])
            i += 1
    return merged, inversions


if __name__ == '__main__':
    f = sys.argv[1]
    numbers = []
    with open(f) as f:
        for line in f:
            num = int(line)
            numbers.append(num)
    print sort(numbers)

