# Courtesy of fenix
import sys

cap = """
.@@@
@@@@
@@@.
@@@@
.@@@
"""

turn = """
@@@@.
@@@@@
@.@@@
@@.@@
.@@@@
"""

def rot90(shape):
    rows = shape.strip().split('\n')
    rotated = [''.join(row[i] for row in reversed(rows)) for i in range(len(rows[0]))]
    return '\n'.join(rotated)

canvas = {}
x, y = 0, 0

def output():
  min_x = min(x for x, y in canvas.keys())
  max_x = max(x for x, y in canvas.keys())
  min_y = min(y for x, y in canvas.keys())
  max_y = max(y for x, y in canvas.keys())
  for j in range(min_y, max_y + 1):
      row = []
      for i in range(min_x, max_x + 1):
          row.append(canvas.get((i, j), '.'))
      print(''.join(row))

def draw(x, y, shape):
    rows = shape.strip().split('\n')
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            canvas[(x + dx, y + dy)] = ch

def vert_conn(x, y, dy, n):
  a = '@@.@@'
  b = '@@@@@'
  for i in range(n):
    draw(x, y + dy * i, a if i % 2 == 0 else b)
  return y + dy * n

def horiz_conn(x, y, dx, n):
  a = '\n'.join('@@.@@')
  b = '\n'.join('@@@@@')
  for i in range(n):
    draw(x + dx * i, y, a if i % 2 == 0 else b)
  return x + dx * n

n = 0

draw(x, y, cap)
x += 4
cur_turn = turn

size = int(sys.argv[1])

for i in range(size):
  n = i*12
  draw(x, y, cur_turn)
  cur_turn = rot90(cur_turn)
  y += 5
  y = vert_conn(x, y, 1, n+1)
  draw(x, y, cur_turn)
  cur_turn = rot90(cur_turn)
  x -= 1
  x = horiz_conn(x, y, -1, n+9)
  draw(x, y, cur_turn)
  cur_turn = rot90(cur_turn)
  y -= 1
  y = vert_conn(x, y, -1, n + 7)
  y -= 4
  draw(x, y, cur_turn)
  cur_turn = rot90(cur_turn)
  x += 5
  x = horiz_conn(x, y, 1, n + 11)

output()
