import string

def parse(filename):
    file = open(filename, 'r')
    text = string.splitfields(string.strip(file.read(100000)), '\n\n')
    eqns = []
    for line in string.splitfields(text[len(text)-1], '\n'):
        nums = string.split(line)
        res = 1
        for i in string.splitfields(nums[0][:-1], 'x'):
            res = res * string.atoi(i)
        nums = nums[1:]
        for i in range(len(nums)):
            nums[i] = string.atoi(nums[i])
        eqns.append((nums, res))
    minos = []
    for mino in text[:-1]:
        count = 0
        for c in mino:
            if c = '#':
                count = count + 1
        minos.append(count)
    return minos, eqns

def solve(minos, eqns):
    res = 0
    for eqn in eqns:
        num = 0
        for i in range(len(minos)):
            num = num + minos[i] * eqn[0][i]
        if num <= eqn[1]:
            res = res + 1
    return res


minos, eqns = parse('input.txt')
print solve(minos, eqns)

