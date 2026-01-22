use strict;
use warnings;

open(my $file,  "<",  "input.txt") or die "joever";
my @intervals = ();
my @cupcakes = ();
while (my $line = <$file>) {
    chomp $line;
    last if $line eq '';
    my ($start, $end) = split(/-/, $line);
    push @intervals, [$start, $end];
}
while (my $line = <$file>) {
    chomp $line;
    push @cupcakes, $line;
}
close $file or die "joever 2: electric boogaloo";

@intervals = sort {$a->[0] <=> $b->[0]} @intervals;
@cupcakes = sort {$a <=> $b} @cupcakes;

my @better_intervals = ();
my ($start, $end) = @{$intervals[0]};
for my $interval (@intervals) {
    my ($s, $e) = @$interval;
    if ($end + 1 < $s) {
        push @better_intervals, [$start, $end];
        $start = $s;
        $end = $e;
    } elsif ($end < $e) {
        $end = $e;
    }
}
push @better_intervals, [$start, $end];

my $p1 = 0;
my $idx = 0;
my $break_flag = 0;
($start, $end) = @{$better_intervals[0]};
for my $cupcake (@cupcakes) {
    while ($end < $cupcake) {
        $idx++;
        if ($idx == @better_intervals) {
            $break_flag = 1;
            last;
        }
        ($start, $end) = @{$better_intervals[$idx]};
    }
    last if $break_flag == 1;
    $p1++ if $cupcake >= $start;
}
print "$p1\n";

my $p2 = 0;
for my $interval (@better_intervals) {
    my ($s, $e) = @$interval;
    $p2 += $e - $s + 1;
}
print "$p2\n";
