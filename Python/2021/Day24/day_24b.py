from typing import Any, Iterable


def parser(testing_input: Any, file_name: str = '', is_testing: bool = False) -> Iterable[list[str | int]]:
    if is_testing:
        if testing_input is None:
            file_to_read = 'test.txt'
        else:
            return testing_input
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        counter = 0
        div, a, b = [], [], []
        for line in file.read().splitlines():
            counter += 1
            if counter == 5:
                div.append(line[6:] == '26')
            elif counter == 6:
                a.append(int(line[6:]))
            elif counter == 16:
                b.append(int(line[6:]))
            elif counter == 18:
                counter = 0
        return div, a, b


def solver(div_list: list[bool], a_list: list[int], b_list: list[int]) -> Any:
    # inp w
    # mul x 0
    # add x z
    # mod x 26
    # div z DIV    div z by 26 or 1
    # add x A
    # eql x w
    # eql x 0
    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y      multiply z by 26 if (original z % 26) + A != w
    # mul y 0
    # add y w
    # add y B
    # mul y x
    # add z y     add to z (w + B) if (original z % 26) + A != w
    stack = []
    digits = [0] * 14
    for i, (div, a, b) in enumerate(zip(div_list, a_list, b_list)):
        if not div:
            stack.append((i, b))
        else:
            popped_i, popped_value = stack.pop()
            offset = a + popped_value
            print(f'[{i}] = [{popped_i}] + {offset}')
            if not offset:
                digits[popped_i] = 1
                digits[i] = 1
            elif offset > 0:
                digits[i] = 1 + offset
                digits[popped_i] = 1
            elif offset < 0:
                digits[i] = 1
                digits[popped_i] = 1 - offset
    print(*enumerate(digits))
    return ''.join([str(i) for i in digits])


def display(num) -> None:
    print(num)


if __name__ == '__main__':
    profiling = False
    test_input = None
    testing = False
    if profiling:
        import cProfile
        import pstats

        with cProfile.Profile() as pr:
            answer = solver(*parser(test_input,
                                    file_name='day_24.txt',
                                    is_testing=testing))
            display(answer)

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename='profiling.prof')
    else:
        answer = solver(*parser(test_input,
                                file_name='day_24.txt',
                                is_testing=testing))
        display(answer)
