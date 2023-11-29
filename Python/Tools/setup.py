import os

from Python.path_stuff import root_path


with open(root_path / 'Tools/template.py', 'r') as file:
    template = file.read()


def make_dir(year: int):
    os.mkdir(root_path / f'{year}')
    for day in range(1, 26):
        os.mkdir(root_path / f'{year}/Day{day}')
        with open(root_path / f'{year}/Day{day}/day_{day}.py', 'w') as file:
            file.write(template.format(day=day, year=year))
        open(root_path / f'{year}/Day{day}/day_{day}.txt', 'x')


if __name__ == '__main__':
    for year in range(2015, 2023):
        for day in range(1, 26):
            os.rename(root_path / f'{year}/Day {day}', root_path / f'{year}/Day{day}')
