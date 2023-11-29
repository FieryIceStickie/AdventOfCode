import time
from collections import deque

from tqdm import tqdm


def parser(filename: str):
    with open(filename, 'r') as file:
        return deque(enumerate(map(int, file.read().splitlines())))


def part_a_solver(liszt: deque):
    zero_idx = next(i for i, v in enumerate(liszt) if not v[1])
    arr = liszt.copy()
    arr.rotate(-zero_idx)
    for i, v in liszt:
        idx = arr.index((i, v))
        # print('start', idx, v, arr)
        arr.rotate(-idx)
        # print('rotate to idx', idx, v, arr)
        arr.popleft()
        # print('pop', idx, v, arr)
        arr.rotate(-v)
        # print('rotate by num', idx, v, arr)
        arr.appendleft((i, v))
        # print('re-insert num', idx, v, arr)
        arr.rotate(-arr.index((zero_idx, 0)))
        # print('re:zero', idx, v, arr, end='\n\n')
    # print(*(arr[i%len(arr)] for i in range(1000, 3001, 1000)))
    return sum(arr[i%len(arr)][1] for i in range(1000, 3001, 1000))

def part_b_solver(liszt: deque):
    liszt = deque((i, v*811589153) for i, v in liszt)
    zero_idx = next(i for i, v in enumerate(liszt) if not v[1])
    arr = liszt.copy()
    arr.rotate(-zero_idx)
    for _ in range(10):
        for i, v in liszt:
            idx = arr.index((i, v))
            # print('start', idx, v, arr)
            arr.rotate(-idx)
            # print('rotate to idx', idx, v, arr)
            arr.popleft()
            # print('pop', idx, v, arr)
            arr.rotate(-v)
            # print('rotate by num', idx, v, arr)
            arr.appendleft((i, v))
            # print('re-insert num', idx, v, arr)
            arr.rotate(-arr.index((zero_idx, 0)))
            # print('re:zero', idx, v, arr, end='\n\n')
    # print(*(arr[i%len(arr)] for i in range(1000, 3001, 1000)))
    return sum(arr[i % len(arr)][1] for i in range(1000, 3001, 1000))


if __name__ == '__main__':
    st = time.perf_counter()
    inputs = parser('day_20.txt')
    print(part_a_solver(inputs))
    # print(part_b_solver(inputs))
    ed = time.perf_counter()
    print(ed-st)
