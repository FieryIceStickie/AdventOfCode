designs = ""
towels = []
File.open("input.txt") { |f|
  designs, _, *towels = f.map(&:chomp)
}
trie = {marked: false}
designs.split(", ") { |design|
  node = trie
  design.each_char { |s|
    if !node.key?(s)
      node[s] = {marked: false}
    end

    node = node[s]
  }
  node[:marked] = true
}

def count(trie, towel)
  cache = {}
  tl = towel.length
  solve = lambda do |idx|
    if idx == tl
      return 1
    elsif cache.key?(idx)
      return cache[idx]
    end

    count = 0
    node = trie
    (idx..tl).each do |i|
      s = towel[i]
      if !node.key?(s)
        break
      end

      node = node[s]
      if node[:marked]
        count += solve.call(i + 1)
      end
    end

    cache[idx] = count
  end

  solve.call(0)
end

p1 = p2 = 0
towels.each do |towel|
  res = count(trie, towel)
  if res > 0
    p1 += 1
  end

  p2 += res
end

puts("#{p1} #{p2}")
