if __name__ == '__main__':
    total = 0
    count = 0
    with open('transaction_log.log', 'r') as f:
        for line in f:
            count = count + 1
            total = total + int(line)

    print total / count
