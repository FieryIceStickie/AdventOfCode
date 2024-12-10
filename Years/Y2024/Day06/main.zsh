#!/bin/zsh

grid=()
x=0
for line in "${(f)"$(<input.txt)"}"; do
    y=0
    gridline=()
    for v in "${(@s::)line}"; do
        if [[ $v == "^" ]]; then
            gx=$x
            gy=$y
        fi
        if [[ $v == "#" ]]; then
            grid+=(1)
        else
            grid+=(0)
        fi
        ((y++))
    done
    ((x++))
done
height=$x
width=$y

inbound() {
    (( 0 <= $1 && $1 < height && 0 <= $2 && $2 < width))
}
get() {
    echo ${grid[$((1 + $1 * height + $2))]}
}

typeset -A visited
px=$gx
py=$gy
dx=-1
dy=0
rotate() {
    local ddx=$dy
    local ddy=$((- dx))
    dx=$ddx
    dy=$ddy
}
while true; do
    visited["${px},${py}"]=1
    ppx=$((px + dx))
    ppy=$((py + dy))
    if ! inbound $ppx $ppy; then
        break
    elif [[ $(get $ppx $ppy) -eq 1 ]]; then
        rotate
    else
        px=$ppx
        py=$ppy
    fi
done
echo ${#visited[@]}

isloop() {
    IFS=',' read -r bx by <<< $1
    bx=${bx#\"}
    by=${by%\"}
    typeset -A seen
    local px=$gx
    local py=$gy
    local dx=-1
    local dy=0
    rotate() {
        local ddx=$dy
        local ddy=$((- dx))
        dx=$ddx
        dy=$ddy
    }
    while true; do
        if [[ -n ${seen["${px},${py},${dx},${dy}"]} ]]; then
            echo 1
            return 1
        fi
        seen["${px},${py},${dx},${dy}"]=1
        ppx=$((px + dx))
        ppy=$((py + dy))
        if ! inbound $ppx $ppy; then
            echo 0
            return 0
        elif [[ $(get $ppx $ppy) -eq 1 || $ppx == $bx && $ppy == $by ]]; then
            rotate
        else
            px=$ppx
            py=$ppy
        fi
    done
}

unset ${visited["${gx},${gy}"]}
blocks=(${(k)visited})
p2=$(echo ${blocks[@]} | tr ' ' '\n' | env_parallel -j 10 isloop | grep -c '^1$')
echo $p2
