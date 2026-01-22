const std = @import("std");
const ArrayList = std.ArrayList;

const Point = packed struct {
    x: i8,
    y: i8,

    pub fn add(self: Point, other: Point) Point {
        return p(self.x + other.x, self.y + other.y);
    }
    pub fn eq(self: Point, other: Point) bool {
        return self.x == other.x and self.y == other.y;
    }
};
const Node = packed struct {
    parent: Point,
    size: i16,
};
const PointCost = packed struct {
    loc: Point,
    cost: i16,
};

fn p(x: i8, y: i8) Point {
    return Point{ .x = x, .y = y };
}

fn pu(x: usize, y: usize) Point {
    const a: i8 = @intCast(x);
    const b: i8 = @intCast(y);
    return p(a, b);
}

fn within(z: Point) bool {
    return 0 <= z.x and z.x < 71 and 0 <= z.y and z.y < 71;
}

var _visited = std.mem.zeroes([71][71]bool);
var dsu = std.mem.zeroes([71][71]Node);

fn visited(z: Point) bool {
    const x: usize = @intCast(z.x);
    const y: usize = @intCast(z.y);
    return _visited[x][y];
}

fn set_visited(z: Point, val: bool) void {
    const x: usize = @intCast(z.x);
    const y: usize = @intCast(z.y);
    _visited[x][y] = val;
}

fn get_dsu_p(z: Point) *Node {
    const x: usize = @intCast(z.x);
    const y: usize = @intCast(z.y);
    return &dsu[x][y];
}

fn get_dsu(z: Point) Node {
    const x: usize = @intCast(z.x);
    const y: usize = @intCast(z.y);
    return dsu[x][y];
}

fn find_set(z: Point) Point {
    const node = get_dsu_p(z);
    if (node.*.parent.eq(z)) {
        return z;
    }
    const res = find_set(node.*.parent);
    node.*.parent = res;
    return res;
}

fn union_set(z1: Point, z2: Point) void {
    var a = find_set(z1);
    var b = find_set(z2);
    if (!a.eq(b)) {
        if (get_dsu(a).size < get_dsu(b).size) {
            const temp = a;
            a = b;
            b = temp;
        }
        get_dsu_p(b).*.parent = a;
        get_dsu_p(a).*.size += get_dsu(b).size;
    }
}

pub fn main() !void {
    const stdout = std.fs.File.stdout.writer();

    var file = try std.fs.cwd().openFile("input.txt", .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();

    const allocator = std.heap.page_allocator;
    var points = ArrayList(Point).init(allocator);
    defer points.deinit();
    var buf: [6]u8 = undefined;
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var it = std.mem.splitScalar(u8, line, ',');
        try points.append(p(
            try std.fmt.parseInt(i8, it.next() orelse "0", 10),
            try std.fmt.parseInt(i8, it.next() orelse "0", 10),
        ));
    }

    for (points.items[0..1024]) |z| {
        set_visited(z, true);
    }

    var p1: i16 = 0;
    var active = std.mem.zeroes([71 * 71]PointCost);
    var s: usize = 0;
    active[s] = PointCost{
        .loc = Point{ .x = 0, .y = 0 },
        .cost = 0,
    };
    s += 1;
    const end = p(70, 70);
    const deltas = [_]Point{ p(-1, 0), p(0, 1), p(1, 0), p(0, -1) };
    var i: usize = 0;
    while (i < s) {
        const node = active[i];
        i += 1;
        if (node.loc.eq(end)) {
            p1 = node.cost;
            break;
        }
        for (deltas) |d| {
            const loc = node.loc.add(d);
            if (within(loc) and !visited(loc)) {
                set_visited(loc, true);
                active[s] = PointCost{
                    .loc = loc,
                    .cost = node.cost + 1,
                };
                s += 1;
            }
        }
    }
    try stdout.print("{}\n", .{p1});

    _visited = std.mem.zeroes([71][71]bool);
    for (points.items) |z| {
        set_visited(z, true);
    }

    var x: usize = 0;
    const upleft = [_]Point{ p(-1, 0), p(0, -1) };
    while (x < 71) {
        var y: usize = 0;
        while (y < 71) {
            const z = pu(x, y);
            if (!visited(z)) {
                dsu[x][y] = Node{ .parent = z, .size = 1 };
                for (upleft) |d| {
                    const loc = z.add(d);
                    if (within(loc) and !visited(loc)) {
                        union_set(z, loc);
                    }
                }
            }
            y += 1;
        }
        x += 1;
    }
    var t = points.items.len - 1;
    const start = p(0, 0);
    while (true) {
        const z = points.items[t];
        get_dsu_p(z).* = Node{ .parent = z, .size = 1 };
        set_visited(z, false);
        for (deltas) |d| {
            const loc = z.add(d);
            if (within(loc) and !visited(loc)) {
                union_set(z, loc);
            }
        }
        if (find_set(start).eq(find_set(end))) {
            break;
        }
        t -= 1;
    }
    try stdout.print("{},{}\n", .{ points.items[t].x, points.items[t].y });
}
