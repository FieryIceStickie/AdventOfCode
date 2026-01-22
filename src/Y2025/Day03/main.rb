banks = []
File.open("input.txt") { |f|
  *banks = f.map(&:chomp)
}

p1 = 0
banks.each do |bank|
  a = -1
  b = -1
  bank.each_char.with_index do |c, i|
    num = c.to_i
    if num > a and i < bank.length - 1
      a = num
      b = -1
    elsif num > b
      b = num
    end
  end

  p1 += 10 * a + b
end

p2_nums = [0] * 12
banks.each do |bank|
  nums = [-1] * 12
  bank.each_char.with_index do |c, i|
    num = c.to_i
    (0..11).each do |j|
      if num > nums[j] and i < bank.length - 11 + j
        nums[j] = num
        nums.fill(-1, j + 1..)
        break
      end
    end
  end

  (0..11).each do |i|
    p2_nums[i] += nums[i]
  end
end

p2 = 0
(0..11).each do |i|
  p2 *= 10
  p2 += p2_nums[i]
end

puts("#{p1} #{p2}")
