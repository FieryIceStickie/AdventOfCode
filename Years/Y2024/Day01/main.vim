" nvim -esS main.vim -c "redir! > /dev/stdout | call Main() | redir END"
function! Part1(left, right)
    let left = sort(copy(a:left))
    let right = sort(copy(a:right))
    let n = 0
    for i in range(0, len(left) - 1)
        let n = n + abs(get(left, i) - get(right, i))
    endfor
    return n
endfunction

function! Part2(left, right)
    let scores = {}
    let score = 0
    let counter = {}
    for num in a:right
        let counter[num] = get(counter, num, 0) + 1
    endfor
    for num in a:left
        if !has_key(scores, num)
            let scores[num] = get(counter, num, 0)
        endif    
        let score = score + num * get(scores, num)
    endfor
    return score
endfunction

function! Parse(path)
    let left = []
    let right = []
    for line in readfile(a:path)
        let [l, r] = split(line)
        call add(left, str2nr(l))
        call add(right, str2nr(r))
    endfor
    return [left, right]
endfunction

function! Main()
    let testing = v:false
    let [left, right] = Parse(testing ? 'test.txt' : 'input.txt')
    echo Part1(left, right)
    echo Part2(left, right)
endfunction
