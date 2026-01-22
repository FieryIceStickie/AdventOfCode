const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.DebugAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    const file = try std.fs.cwd().openFile("input.txt", .{ .mode = .read_only });
    defer file.close();
    var buf: [142]u8 = undefined;
    var reader = file.reader(&buf);
    var line = std.Io.Writer.Allocating.init(alloc);
    defer line.deinit();

    const nc = 70;
    const tn = @divFloor(nc * (nc+1), 2);
    var dp = [_]u64{0} ** (tn);
    dp[0] = 1;
    var row: i16 = -2;
    var t: usize = 0;
    var p1: u64 = 0;
    var p2: u64 = 0;

    while (true) {
        _ = reader.interface.streamDelimiter(&line.writer, '\n') catch |err| {
            if (err == error.EndOfStream) break else return err;
        };
        reader.interface.toss(1);
        if (@rem(row, 2) == 1 or row < 0) {
            line.clearRetainingCapacity();
            row += 1;
            continue;
        }
        const x: usize = @intCast(@divFloor(row, 2));
        var y: usize = 0;
        while (y <= x) {
            const c = line.written()[nc + 2*y - x] == '^';
            const n = t + y;
            const l = t + if (c) x + 1 else 2*x+3;
            if (dp[n] > 0) {
                if (c) p1 += 1;
                if (l < tn) {
                    if (c) dp[l + y] += dp[n];
                    dp[l + y + 1] += dp[n];
                } else {
                    p2 += (if (c) 2 * dp[n] else dp[n]);
                }
            }
            y += 1;
        }
        t += x + 1;
        line.clearRetainingCapacity();
        row += 1;
    }
    std.debug.print("{d} {d}\n", .{p1, p2});
}
