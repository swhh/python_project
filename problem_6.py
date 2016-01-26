from sys import argv


def two_sum_total(numbers, start, finish):
    total = 0
    for i in xrange(start, finish + 1):
        if two_sum(numbers, i):
            total += 1

    return total


def two_sum(numbers, target):
    for num in numbers.iterkeys():
        if (target - num) != num and numbers.get(target - num):
            return True

    return False


if __name__ == '__main__':
    f = argv[1]
    numbers = dict()
    with open(f) as f:
        for line in f:
            numbers[int(line)] = 1
    print two_sum(numbers, 150)




