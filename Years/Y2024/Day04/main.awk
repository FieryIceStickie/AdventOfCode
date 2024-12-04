#!/bin/awk -f
BEGIN {
    p1 = 0;
    p2 = 0;
}

{
    for (i = 1; i <= length($0); i++) {
        char = substr($0, i, 1);
        grid[NR, i] = char == "X" ? 0 : char == "M" ? 1 : char == "A" ? 2 : 3;
    }
    height = NR;
    width = length($0);
}

function p1s(i1, j1, i2, j2, i3, j3, i4, j4) {
    if (!(1 <= i4 && i4 <= height && 1 <= j4 && j4 <= width)) {
        return 0;
    }
    p1v = grid[i1, j1] + 4 * grid[i2, j2] + 16 * grid[i3, j3] + 64 * grid[i4, j4];
    return p1v == 27 || p1v == 228;
}

function get(m, n) {
    v = grid[m, n];
    return v == 0 ? 2 : v == 1 ? 1 : v == 2 ? 16 : -1;
}

END {
    for (i = 1; i <= height; i++) {
        for (j = 1; j <= height; j++) {
            p1 += p1s(i, j, i, j+1, i, j+2, i, j+3);
            p1 += p1s(i, j, i+1, j, i+2, j, i+3, j);
            p1 += p1s(i, j, i+1, j+1, i+2, j+2, i+3, j+3);
            p1 += p1s(i, j, i+1, j-1, i+2, j-2, i+3, j-3);
        }
    }

    for (i = 2; i <= height - 1; i++) {
        for (j = 2; j <= height - 1; j++) {
            p2v = 16 * get(i, j) + get(i-1, j-1) + get(i+1, j+1) + 4 * (get(i+1, j-1) + get(i-1, j+1));
            p2 += p2v == 256;
        }
    }
    print p1 " " p2;
}
