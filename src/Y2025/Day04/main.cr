grid = {} of Tuple(Int32, Int32) => Bool
x = 0
File.open("evil.txt").each_line(chomp=true) do |line|
  line.each_char.with_index do |elem, y|
    grid[{x, y}] = elem == '@'
  end
  x += 1
end

p1 = 0
values = {} of Tuple(Int32, Int32) => Int32
grid.each do |(x, y), v|
  if !v
      next
  end
  s = 0
  (-1..1).each do |dx|
    (-1..1).each do |dy|
      if grid.fetch({x + dx, y + dy}, false)
        s += 1
      end
    end
  end
  if s <= 4
    p1 += 1
  end
  values[{x, y}] = s - 1
end

def remove(grid, values, x, y)
  if !grid.fetch({x, y}, false)
    return 0
  end
  if values[{x, y}] > 3
    return 0
  end
  grid[{x, y}] = false
  s = 1
  (-1..1).each do |dx|
    (-1..1).each do |dy|
      p = {x + dx, y + dy}
      if values.fetch(p, false)
        values[p] -= 1
      end
    end
  end
  (-1..1).each do |dx|
    (-1..1).each do |dy|
      s += remove(grid, values, x + dx, y + dy)
    end
  end
  return s
end

p2 = 0
grid.each do |(x, y), v|
  p2 += remove(grid, values, x, y)
end

puts p1, p2
