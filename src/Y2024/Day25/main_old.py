def parse(filename):
    file = open(filename, 'r')
    locks = []
    keys = []
    while 1:
        line = file.readline()
        if line = '#####\n':
            s = locks
        else:
            s = keys
        item = range(25)
        for x in range(5):
            line = file.readline()
            for y in range(5):
                if line[y] = '#':
                    item[x + 5 * y] = -1
        s.append(item)
        _ = file.readline()
        if not file.readline():
            break
    file.close()
    return locks, keys

def solve(locks, keys):
    s = 0
    for lock in locks:
        for key in keys:
            b = 1
            for i in range(25):
                if lock[i] = key[i] = -1:
                    b = 0
                    break
            s = s + b
    return s

locks, keys = parse('input.txt')
solve(locks, keys)
