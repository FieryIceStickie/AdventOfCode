import os
import regex
import arrays

struct Point {
    x int
    y int
}


fn Point.new(x int, y int) Point {
    return Point{(101 + x) % 101, (103 + y) % 103}
}

fn (p Point) add(q Point) Point {
    return Point.new(p.x + q.x, p.y + q.y)
}

fn (p Point) hash() int {
    return p.x + 101 * p.y
}

struct Bot {
mut:
    pos Point
    vel Point
}

fn (mut bot Bot) move() {
    bot.pos = bot.pos.add(bot.vel)
}

fn main() {
    mut data := parse('input.txt')!
    p1, p2 := solve(mut data)!
    println(p1)
    println(p2)
}

fn parse(filename string) ![]Bot {
    f := os.read_file(filename)!
    mut bots := []Bot{}
    mut re := regex.regex_opt("-?\\d+") or { panic(err) }
    for line in f.split_into_lines() {
        m := re.find_all_str(line)
        p := Point.new(m[0].int(), m[1].int())
        v := Point.new(m[2].int(), m[3].int())
        bots << Bot{p, v}
    }
    return bots
}

fn solve(mut bots []Bot) !(int, int) {
    mut p1 := 0
    mut xt := 0
    mut x_max := 0
    mut yt := 0
    mut y_max := 0
    for t in 1 .. 103 {
        for mut bot in bots {
            bot.move()
        }
        if t == 100 {
            p1 = solvep1(bots)
        }
        mx := arrays.max(
            arrays.map_of_counts(bots.map(|bot| bot.pos.x)).values()
        )!
        if mx > x_max {
            xt = t
            x_max = mx
        }
        my := arrays.max(
            arrays.map_of_counts(bots.map(|bot| bot.pos.y)).values()
        )!
        if my > y_max {
            yt = t
            y_max = my
        }
    }
    xt = xt % 101
    yt = yt % 103
    return p1, xt + (10403 + yt - xt) * 5151 % 10403
}

fn solvep1(bots []Bot) int {
    mut counts := map[int]int{}
    for bot in bots {
        mut c := 0
        if bot.pos.x < 50 {
            c += 1
        } else if bot.pos.x > 50 {
            c -= 1
        }
        if bot.pos.y < 51 {
            c += 3
        } else if bot.pos.y > 51 {
            c -= 3
        }
        if c in [-4, -2, 2, 4] {
            counts[c] += 1
        }
    }
    return arrays.fold(counts.values(), 1, |x, y| x * y)
}
