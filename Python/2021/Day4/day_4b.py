from typing import Any

import numpy as np


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return file.read().splitlines()
    if len(inputs) == 0 and testing:
        with open('test.txt', 'r') as file:
            return file.read().splitlines()
    return inputs


def solver(inputs: Any) -> Any:
    bingo_numbers = np.array(inputs[0].split(','), dtype=int)
    bingo_boards = np.array(inputs[1:], dtype=str).reshape((-1, 6))
    for i in bingo_boards:
        Board(i[1:])
    board, num = bingo_iter(bingo_numbers)
    inverted_mark_board = ~board.mark_board + 2
    score = num * np.sum(np.where(inverted_mark_board, board.board, inverted_mark_board))
    return score


class Board:
    all_boards = []

    def __init__(self, rows: np.ndarray):
        self.board = np.array([i.split() for i in rows], dtype=int)
        self.mark_board = np.zeros((5, 5), dtype=int)
        self.all_boards.append(self)

    def mark_num(self, num: int) -> 0 | 1:
        idx = np.nonzero(self.board == num)
        self.mark_board[idx] = 1
        if self.check_win():
            return 1
        return 0

    def check_win(self) -> 0 | 1:
        if 5 in np.sum(self.mark_board, axis=1) or 5 in np.sum(self.mark_board, axis=0):
            return 1
        return 0


def bingo_iter(bingo_numbers: np.ndarray) -> (Board, int):
    for num in bingo_numbers:
        if len(Board.all_boards) != 1:
            won_boards = []
            for board in Board.all_boards:
                if board.mark_num(num):
                    won_boards.append(board)
            for won_board in won_boards:
                Board.all_boards.remove(won_board)
        else:
            board = Board.all_boards[0]
            if board.mark_num(num):
                return board, num


def display(score) -> None:
    print(score)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='day_4.txt',
        testing=False))
    display(answer)
