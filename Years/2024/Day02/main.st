| part1 part2 main |
Collection extend [
    any: func [
        self do: [ :elem | (func value: elem) ifTrue: [^true] ].
        ^false.
    ]

    count: func [
        | c |
        c := 0.
        self do: [ :elem | (func value: elem) ifTrue: [c := c + 1]].
        ^c.
    ]

    diff [
        ^(1 to: self size - 1) collect: [:i | (self at: (i+1)) - (self at: i)].
    ]

    exclude: idx [
        ^(1 to: self size - 1) collect: [ :i | 
            self at: i + ((i >= idx) ifTrue: [1] ifFalse: [0])
        ].
    ]

    isGood [
        | sgn |
        sgn := (self at: 1) sign.
        ^self allSatisfy: [:d | (d sign = sgn) & (d abs between: 1 and: 3)].
    ]
].
String extend [
    splitInts [
        ^(self tokenize: ' ') collect: [ :each | each asInteger ].
    ]
].
FileStream extend [
    parse [
        | lines |
        lines := OrderedCollection new.
        self linesDo: [ :line | lines addLast: line splitInts ].
        ^lines.
    ]
].

part1 := [ :levels | levels count: [ :level | level diff isGood ] ].
part2 := [ :levels | levels count: [ :level | 
    (1 to: level size) any: [ :i | (level exclude: i) diff isGood]
] ].

main := [
    testing := false.
    filename := testing ifTrue: ['test.txt'] ifFalse: ['input.txt'].
    file := FileStream open: filename mode: #read.
    data := file parse.
    file close.
    Transcript
        show: (part1 value: data) printString; cr;
        show: (part2 value: data) printString; cr.
].
main value.
