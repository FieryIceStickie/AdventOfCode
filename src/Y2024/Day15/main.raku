sub parse(\filename) {
    my %move_dict = '^' => -1, '>' => 1i, 'v' => 1, '<' => -1i;
    my ($maze_str, $move_str) = (slurp filename).split("\n\n");
    $move_str .= subst("\n", :g);
    my @moves = $move_str.comb.map({ %move_dict{$_} });

    my SetHash $grid .= new;
    my SetHash $boxes .= new;
    my $bot;
    for $maze_str.split("\n").kv -> $x, $row {
        for $row.comb.kv -> $y, $v {
            my $z = $x + 1i * $y;
            if $v eq "@" {
                $bot = $z;
            } elsif $v eq "#" {
                $grid.set($z);
            } elsif $v eq "O" {
                $boxes.set($z);
            }
        }
    }
    return [$grid, $boxes, @moves, $bot];
}

sub p1solve($g, $b, @moves, $bot) {
    my $grid = $g.clone;
    my $boxes = $b.clone;
    my $z = $bot;
    for @moves -> $move {
        $z += $move;
        my $can_move = !$grid{$z};
        if $boxes{$z} {
            my $bz = $z;
            repeat {
                $bz += $move;
            } while $boxes{$bz};
            $can_move = !$grid{$bz};
            if $can_move {
                $boxes{$z} = !$boxes{$z};
                $boxes{$bz} = !$boxes{$bz};
            }
        }
        $z -= $move if !$can_move;
    }
    return $boxes.kv.map(-> $z0, $_ { 100 * $z0.re + $z0.im }).sum;
}

sub push($box, $d, $cache, $grid, $boxes) {
    return True if $cache{$box};
    $cache.set($box);
    return False if $grid{$box + $d};
    return False if $grid{$box + $d + 1i/2};
    my @bxs = [];
    if $d ~~ Int {
        for -1i/2, 0, 1i/2 -> $dy {
            @bxs.append($box + $d + $dy);
        }
    } else {
        @bxs.append($box + 2 * $d);
    }
    for @bxs -> $bx {
        return False if $boxes{$bx} and !push($bx, $d, $cache, $grid, $boxes);
    }
    return True;
}

sub p2solve($g, $b, @moves, $bot) {
    my SetHash $grid .= new;
    for $g.kv -> $k, $_ {
        $grid.set($k);
        $grid.set($k + 1i/2);
    }
    my $boxes = $b.clone;
    my $z = $bot;

    for @moves.kv -> $i, $m {
        my $move;
        if $m ~~ Int {
            $move = $m;
        } else {
            $move = $m / 2;
        }
        $z += $move;
        my $can_move = !$grid{$z};
        my SetHash $cache .= new;
        my $s;
        $s = $z if $boxes{$z};
        $s = $z - 1i/2 if $boxes{$z - 1i/2};
        if $s.defined {
            $can_move = push($s, $move, $cache, $grid, $boxes);
            if $can_move {
                for $cache.kv -> $l, $_ {
                    $boxes{$l} = !$boxes{$l};
                    $boxes{$l + $move} = !$boxes{$l + $move};
                }
            }
        }
        $z -= $move if !$can_move;
    }
    return $boxes.kv.map(-> $z0, $_ { 100 * $z0.re + 2 * $z0.im }).sum;
}

sub main() {
    my ($grid, $boxes, $moves, $bot) = parse('input.txt');
    my $p1 = p1solve($grid, $boxes, $moves, $bot);
    my $p2 = p2solve($grid, $boxes, $moves, $bot);
    print $p1, " ", $p2, "\n";
}

main();

