import std.stdio : writeln;
import std.algorithm.iteration : map, sum;
import std.array : split, array;
import std.conv : to;
import std.file : readText;
import std.functional : memoize;

ulong count(ulong s, ulong n) {
    if (n == 0) {
        return 1;
    }
    if (s == 0) {
        return memoize!count(1, n-1);
    } 
    auto ns = to!string(s);
    if (ns.length % 2) {
        return memoize!count(s * 2024, n-1);
    }
    auto m = ns.length / 2;
    return memoize!count(to!ulong(ns[0..m]), n-1) + memoize!count(to!ulong(ns[m..ns.length]), n-1);
}

void main() {
    ulong[] stones = readText("input.txt")
        .split(" ")
        .map!(v => to!ulong(v))
        .array();
    ulong p1 = stones.map!(s => count(s, 25)).sum!();
    ulong p2 = stones.map!(s => count(s, 75)).sum!();
    writeln(p1);
    writeln(p2);
}
