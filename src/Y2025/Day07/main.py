from typing import TextIO


def parser(raw_data: TextIO) -> list[str]:
    return raw_data.read().splitlines()


def full_solver(lines: list[str]) -> tuple[int, int]:
    it = iter(lines)
    nc = next(it).index('S')
    tn = nc * (nc+1) // 2
    dp = [0] * tn
    dp[0] = 1
    _ = next(it)
    t = 0
    p1 = p2 = 0
    for x, line in enumerate(it):
        for y in range(0, x+1):
            c = line[nc + 2*y - x] == '^'
            n = t + y
            l = t + (x + 1 if c else 2*x + 3)
            if dp[n] > 0:
                p1 += c
                if l < tn:
                    dp[l+y] += c * dp[n]
                    dp[l+y+1] += dp[n]
                else:
                    p2 += dp[n] * (2 if c else 1)
        _ = next(it)
        t += x + 1
    return p1, p2


if __name__ == "__main__":
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = "input.txt"
    else:
        path = test_path if testing else "input.txt"

    with open(path, "r") as file:
        data = parser(file)

    print(*full_solver(data))
