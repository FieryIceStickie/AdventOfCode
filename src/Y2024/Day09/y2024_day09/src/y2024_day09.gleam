import gleam/io
import gleam/string
import gleam/list
import gleam/int
import gleam/result

import file_streams/file_stream

pub fn main() {
    let assert Ok(line) = "../input.txt"
    |> file_stream.open_read
    |> result.try(file_stream.read_line)
    let assert Ok(disk) = line
    |> string.split("")
    |> list.try_map(int.parse)

    [p1, p2]
    |> list.map(fn (func) { func(disk) })
    |> list.map(int.to_string)
    |> string.join(" ")
    |> io.println
}

type ID {
    Some(Int)
    None
}

fn get_id(id: Int) -> ID {
    case id % 2 {
        0 -> Some(id / 2)
        _ -> None
    }
}

fn p1(disk: List(Int)) -> Int {
    let disk = disk
    |> list.index_map(fn (n, id) { list.repeat(id |> get_id, n) })
    |> list.flatten

    p1c(disk |> enumerate, disk |> enumerate |> list.reverse,  0)
}

fn enumerate(l: List(v)) -> List(#(Int, v)) {
    l |> list.index_map(fn (v, i) { #(i, v) })
}

fn p1c(front: List(#(Int, ID)), back: List(#(Int, ID)), accum: Int) -> Int {
    let back = list.drop_while(back, fn(v) {v.1 == None})
    case front, back {
        [#(i, _), ..], [#(j, _), ..] if i > j -> accum
        [#(i, None), ..ft], [#(_, Some(b)), ..bt] -> p1c(ft, bt, accum + i * b)
        [#(i, Some(f)), ..ft], _ -> p1c(ft, back, accum + i * f)
        _, _ -> -1
    }
}

type ISD = List(#(Int, Int, ID))
type Holes = List(#(Int, Int))

fn p2(disk: List(Int)) -> Int {
    let #(_, disk) = disk 
    |> list.index_map(fn (n, id) { #(n, id |> get_id) })
    |> list.map_fold(0, fn(idx, v) { 
        let #(n, id) = v
        #(idx + n, #(idx, n, id)) 
    })
    let front : Holes = disk |> list.filter_map(fn(v) {
        case v {
            #(_, _, Some(_)) -> Error(Nil)
            #(idx, size, None) -> Ok(#(idx, size))
        }
    })

    p2c(front, disk |> list.reverse, 0)
}

fn sum_range(start: Int, stop: Int) {
    { stop - start } * { stop + start - 1 } / 2
}

fn p2c(front: Holes, back: ISD, accum: Int) -> Int {
    case back {
        [] -> accum
        [#(_, _, None), ..bt] -> p2c(front, bt, accum)
        [#(idx, size, Some(id)), ..bt] -> {
            let #(front, value) = p2p(front, size, idx, list.new())
            p2c(front, bt, accum + id * value)
        }
    }
}

fn p2p_default(size: Int, idx: Int, accum: Holes) -> #(Holes, Int) {
    #(accum |> list.reverse, sum_range(idx, idx + size))
}

fn p2p(front: Holes, size: Int, idx: Int, accum: Holes) -> #(Holes, Int) {
    case front {
        [] -> p2p_default(size, idx, accum)
        [#(fidx, _), ..] if fidx >= idx -> p2p_default(size, idx, accum)
        [#(fidx, fsize), ..ft] if fsize < size -> p2p(ft, size, idx, [#(fidx, fsize), ..accum])
        [#(fidx, fsize), ..ft] -> #(case size == fsize {
            True -> [accum |> list.reverse, ft]
            False -> [accum |> list.reverse, [#(fidx + size, fsize - size)], ft]
        } |> list.flatten, sum_range(fidx, fidx + size))
    }
}
