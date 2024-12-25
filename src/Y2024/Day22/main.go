package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var data []int
	for scanner.Scan() {
		n, err := strconv.Atoi(scanner.Text())
		if err != nil {
			panic(err)
		}
		data = append(data, n)
	}
    fmt.Println(solve(data))
}

func next(n *int) {
	*n ^= (*n) << 6 & 0xffffff
	*n ^= (*n) >> 5 & 0xffffff
	*n ^= (*n) << 11 & 0xffffff
}

func solve(data []int) (p1, p2 int) {
	p1 = 0
	p2_arr := make([]int, 130321)
	for _, num := range data {
        seen := make([]bool, 130321)
        window := make([]int, 4)
        for i := range window {
            window[3 - i] = num % 10
            next(&num)
        }
        diffs := make([]int, 3)
        for i := range diffs {
            diffs[i] = 9 + window[i] - window[i + 1]
        }
        diff := diffs[0] + diffs[1] * 19 + diffs[2] * 19 * 19
        prev := window[0]
        m := 0
        for i := 0; i < 1996; i++ {
            price := num % 10
            next(&num)
            diff = 9 + price - prev + diff * 19 % 130321
            prev = price
            if seen[diff] {
                continue
            }
            seen[diff] = true
            if price != 0 {
                p2_arr[diff] += price
            }
            m++
        }
        p1 += num
	}
    p2 = 0
    for _, num := range p2_arr {
        p2 = max(p2, num)
    }
    return
}
