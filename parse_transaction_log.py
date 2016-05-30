import sys

if __name__ == '__main__':
    total = 0
    count = 0
    cur_min = 9999999
    cur_max = 0
    with open(sys.argv[1], 'r') as f:
        for line in f:
            count = count + 1
            value = int(line)
            total = total + value
            cur_min = min(cur_min, value)
            cur_max = max(cur_max, value)

    print 'avg: ', total / count, ' min: ', cur_min, ' max: ', cur_max
