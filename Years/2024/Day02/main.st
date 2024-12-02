| part1 part2 diffArr diffSkip parse main |
part1 := [ :levels |
    | c |
    c := 0.
    levels do: [ :level |
        diff := diffArr value: level.
        sgn := (diff at: 1) sign.
        b := diff allSatisfy: [:d | (d sign = sgn) & (d abs between: 1 and: 3)].
        b ifTrue: [c := c + 1].
    ].
    c.
].
part2 := [ :levels |
    | c |
    c := 0.
    levels do: [ :level |
        result := (Interval from: 1 to: (level size)) detect: [ :skip |
            diff := diffSkip value: level value: skip.
            sgn := (diff at: 1) sign.
            diff allSatisfy: [:d | (d sign = sgn) & (d abs between: 1 and: 3)].
        ] ifNone: [nil].
        result ifNotNil: [c := c + 1].
    ].
    c.
].
diffArr := [ :arr | 
    | diff |
    diff := Array new: (arr size - 1).
    1 to: (diff size) do: [:i | diff at: i put: ((arr at: (i+1)) - (arr at: i))].
    diff.
].
diffSkip := [ :arr :skip | 
    | diff |
    diff := Array new: (arr size - 2).
    1 to: (diff size) do: [:i | 
        step := [:i | (i >= skip) ifTrue: [i+1] ifFalse: [i]].
        diff at: i put: ((arr at: (step value: (i+1))) - (arr at: (step value: i))).
    ].
    diff.
].
parse := [ :file |
    | lines |
    lines := OrderedCollection new.
    file linesDo: [ :line | 
        lines addLast: ((line tokenize: ' ') collect: [ :each | each asInteger])
    ].
    lines.
].
main := [
    testing := false.
    filename := testing ifTrue: ['test.txt'] ifFalse: ['input.txt'].
    file := FileStream open: filename mode: #read.
    data := parse value: file.
    file close.
    Transcript
        show: (part1 value: data) printString; cr;
        show: (part2 value: data) printString; cr.
].
main value.
