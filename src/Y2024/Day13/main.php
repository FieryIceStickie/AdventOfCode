<?php
$inp = file_get_contents('input.txt');
$num_matches = preg_match_all(
    '/(?sU)Button A.*X\+(\d+?).*(\d+?).*(\d+?).*(\d+?).*(\d+?).*(\d+?)/', 
    $inp, $data
);
$p1 = $p2 = 0;

function calc($a, $b, $c, $d, $u1, $u2) {
    $det = $a*$d - $b*$c;
    $sgn = $det < 0 ? -1 : 1;
    $det *= $sgn;
    $x1 = $d * $u1 - $b * $u2;
    $x2 = -$c * $u1 + $a * $u2;
    $x1 *= $sgn;
    $x2 *= $sgn;
    if ($x1 < 0 || $x2 < 0) {
        return 0;
    }
    $q1 = intdiv($x1, $det);
    $q2 = intdiv($x2, $det);
    $r1 = $x1 % $det;
    $r2 = $x2 % $det;
    if ($r1 != 0 || $r2 != 0) {
        return 0;
    }
    return 3 * $q1 + $q2;
}
$m = 10000000000000;

for ($i = 0; $i < $num_matches; $i++) {
    $a = $data[1][$i];
    $c = $data[2][$i];
    $b = $data[3][$i];
    $d = $data[4][$i];
    $v1 = $data[5][$i];
    $v2 = $data[6][$i];
    $p1 += calc($a, $b, $c, $d, $v1, $v2);
    $p2 += calc($a, $b, $c, $d, $v1 + $m, $v2 + $m);
}
echo $p1, ' ', $p2, "\n";
?>
