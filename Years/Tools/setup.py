import os

import requests

from Years.path_stuff import root_path

with open(root_path / 'Tools/template.py', 'r') as file:
    template = file.read()


def make_dir(year: int):
    os.mkdir(root_path / f'{year}')
    for day in range(1, 26):
        os.mkdir(root_path / f'{year}/Day{day}')
        with open(root_path / f'{year}/Day{day}/code.py', 'w') as file:
            file.write(template.format(day=day, year=year))
        open(root_path / f'{year}/Day{day}/input.txt', 'x').close()


def make_txt(year: int):
    for day in range(1, 26):
        open(root_path / f'{year}/Day{day}/input.txt', 'x').close()


def make_golf():
    os.mkdir(root_path / 'Golf')
    for i in range(1, 4):
        open(root_path / f'Golf/golf_{i}.py', 'x').close()
        open(root_path / f'Golf/golf_{i}.txt', 'x').close()


def fill_text(year: int, token: str):
    for day in range(1, 26):
        response = requests.get(url=f'https://adventofcode.com/{year}/day/{day}/input',
                                cookies={'session': token})
        if not response.ok:
            raise ValueError('requests errored')
        with open(root_path / f'{year}/Day{day}/code.txt', 'w') as file:
            file.write(response.text)


if __name__ == '__main__':
    pass
