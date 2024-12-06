variable file
s" input.txt" r/o open-file drop file !

256 Constant max-line
create line max-line 2 + chars allot

: read ( -- n ) line max-line file @ read-line 2drop ;

variable rulesl 2000 cells allot
variable rulesr 2000 cells allot
variable ruleidx 0 ruleidx !

: parse-digit ( addr -- addr n ) dup c@ 48 - ;
: parse-two-digit ( addr -- n addr ) parse-digit 10 * swap char+ parse-digit rot + swap char+ ;
: parse-digits ( -- m n ) line parse-two-digit char+ parse-two-digit drop ;

: push ( n addr idx -- ) cells + ! ;

: write-rule ( -- ) parse-digits rulesr ruleidx @ push rulesl ruleidx @ push ;
: read-rules ( -- ) BEGIN read 0 > WHILE write-rule 1 ruleidx +! REPEAT ;

: cmpcompact ( n m -- s ) 2dup > if swap then 100 * + ;
: cmploop ( s addrl addrr -- addr1 addr2 )
    BEGIN
    dup @ 2>R dup @ 2R> rot cmpcompact 3 pick <>
    WHILE
    1 cells + swap 1 cells + swap
    REPEAT rot drop ;
: cmpend ( n m addr1 addr2 -- r ) drop @ >R drop R> = IF 1 ELSE 0 THEN ;
: cmp ( n m -- r ) 2dup cmpcompact rulesl rulesr cmploop cmpend ;

create p1 1 cells allot 0 p1 !
create p2 1 cells allot 0 p2 !
create numpair 1 cells allot

: write-update ( n -- .. ) line parse-two-digit rot 0 ?do char+ parse-two-digit loop drop ;
: median ( -- med ) numpair @ 2 / pick ;
: ndup ( xn ... x0 n -- xn ... x0 xn ... x0 ) dup dup >R 0 ?do i pick pick loop R> roll drop ;
: order-reduce ( m n b -- m b ) >R >R dup R> cmp R> * ;
: check-sorted ( .. - .. s ) numpair @ 1 + ndup 1 numpair @ 0 ?do order-reduce loop swap drop ;

create sortflag

: disp ( -- ) p1 ? p2 ? ;

: lroll ( -- ) numpair @ roll ;
: *! ( n addr -- ) dup >R @ * R> ! ;
: sortcmp ( m n -- m n ) 2dup cmp dup sortflag *! if else swap then ;
: sort ( .. -- .. ) 
    BEGIN 
    1 sortflag ! lroll 
    numpair @ 0 ?do 
    lroll sortcmp 
    loop sortflag @ UNTIL ;

: update-res ( .. -- ) check-sorted if median p1 +! else sort median p2 +! then clearstack ;
: read-updates ( -- ) BEGIN read dup 0 > WHILE 3 / dup numpair ! write-update update-res REPEAT ;

read-rules
read-updates
disp

clearstack

