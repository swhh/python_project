from sys import argv

comps = 0


def quicksort(l):
    recursive_quicksort(0, len(l) - 1, l)


def recursive_quicksort(lo, hi, l):
    global comps
    if lo >= hi:
        return
    pivot = merge(lo, hi, l)
    comps = comps + (hi - lo)
    recursive_quicksort(lo, pivot - 1, l)
    recursive_quicksort(pivot + 1, hi, l)


def merge(lo, hi, l):
    i = hi - 1
    j = hi - 1
    pivot = l[hi]
    while j > lo - 1:
        if pivot > l[j]:
            j -= 1
            continue
        swap(i, j, l)
        i -= 1
        j -= 1
    swap(hi, i + 1, l)
    return i + 1


def swap(i, j, l):
    swp = l[i]
    l[i] = l[j]
    l[j] = swp


if __name__ == '__main__':
    f = argv[1]
    l = []
    with open(f) as f:
        for line in f:
            l.append(int(line))
    quicksort(l)
    print comps




