import std/sets
import std/strutils
import std/strformat
import std/enumerate
import std/heapqueue
import std/tables
import std/options
import fusion/matching

type 
    Complex = tuple
        x: int
        y: int
    LocFacing = tuple
        loc: Complex
        facing: Complex
    Path = tuple
        loc_facing: LocFacing
        num_tiles: int
        num_turns: int
    Graph = Table[Complex, Table[Complex, Path]]
    PrioNode = tuple
        cost: int
        num_tiles: int
        loc_facing: LocFacing
        pred: Option[LocFacing]
    VisitedNode = tuple
        cost: int
        tile_count: int
        preds: HashSet[LocFacing]

proc make_visited(cost: int): VisitedNode = (cost, 0, initHashSet[LocFacing]())

proc `+`(z1, z2: Complex): Complex = (z1.x + z2.x, z1.y + z2.y)

proc `*`(z1, z2: Complex): Complex = (z1.x * z2.x - z1.y * z2.y, z1.x * z2.y + z2.x * z1.y)

proc `-`(z: Complex): Complex = (-z.x, -z.y)

proc `<`(p, q: PrioNode): bool = p.cost < q.cost

var deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

proc collapse_grid(grid: HashSet[Complex], forced: var HashSet[Complex]): Graph =
    var start = forced.pop
    var
        active: seq[LocFacing] = @[]
        graph = initTable[Complex, Table[Complex, Path]]()
        visited = initHashSet[LocFacing]()
    graph[start] = initTable[Complex, Path]()
    for d in deltas:
        if start + d notin grid:
            active.add((start, d))
    while active.len > 0:
        let (loc, facing) = active.pop
        if (loc, facing) in visited:
            continue
        var
            z = loc
            d = facing
            num_tiles = 0
            num_turns = 0
            is_dead_end = false
            s: seq[Complex] = @[]
        while true:
            z = z + d
            inc(num_tiles)
            if z in forced:
                break
            s = @[]
            for dz in [(0, 1), (1, 0), (0, -1)]:
                if z + dz * d notin grid:
                    s.add(dz * d)
            case s.len
            of 0: 
                is_dead_end = true 
                break
            of 1: discard
            else: break
            let new_d = s.pop
            if new_d != d:
                d = new_d
                inc(num_turns)
        if is_dead_end: continue
        visited.incl((loc, facing))
        visited.incl((z, -d))
        graph[loc][facing] = ((z, d), num_tiles, num_turns)
        graph.mgetOrPut(z)[-d] = ((loc, -facing), num_tiles, num_turns)
        for d in s:
            active.add((z, d))
    return graph

proc parse(filename: string): (Graph, Complex, Complex) =
    var
        grid = initHashSet[Complex]()
        start, goal: Complex
    for x, row in enumerate(readFile(filename).splitLines()):
        for y, v in enumerate(row):
            let z: Complex = (x, y)
            case v
            of 'S': start = z
            of 'E': goal = z
            of '#': grid.incl(z)
            else: discard
    var forced = toHashSet([start, goal])
    return (collapse_grid(grid, forced), start, goal)

proc count_tiles(visited: Table[LocFacing, VisitedNode], ends: HashSet[LocFacing]): int =
    var
        p2 = 0
        cache = initTable[Complex, HashSet[Complex]]()

    proc visit(node: LocFacing) = 
        if node.facing in cache.mgetOrPut(node.loc):
            return
        cache[node.loc].incl(node.facing)
        p2 += visited[node].tile_count
        for pred in visited[node].preds:
            visit(pred)

    for goal in ends:
        visit(goal)
    return p2 + len(cache)

proc solve(graph: Graph; start, goal: Complex): (int, int) =
    var
        loc_facing = (start, (0, 1))
        active: HeapQueue[PrioNode] = [(0, 1, loc_facing, none(LocFacing))].toHeapQueue
        visited = initTable[LocFacing, VisitedNode]()
        p1 = none(int)
        ends = initHashSet[LocFacing]()
    while active.len > 0:
        let node = active.pop()
        case p1
        of Some(@p):
            if node.cost > p:
                break
        of None(): discard

        var has_visited = false
        if node.loc_facing in visited:
            if visited[node.loc_facing].cost < node.cost:
                continue
            has_visited = true
        else:
            visited[node.loc_facing] = make_visited(node.cost)
        case node.pred:
        of Some(@p):
            visited[node.loc_facing].preds.incl(p)
        of None(): discard
        inc(visited[node.loc_facing].tile_count, node.num_tiles - 1)
        if has_visited: continue

        if node.loc_facing.loc == goal:
            p1 = some(node.cost)
            ends.incl(node.loc_facing)
            continue

        for facing, (loc_facing, num_tiles, num_turns) in graph[node.loc_facing.loc].pairs:
            var
                new_cost: int
                new_loc_facing: LocFacing
                new_num_tiles: int
            let pred = node.pred.get(((-1, -1), (0, 0))).loc
            if facing == node.loc_facing.facing:
                new_cost = node.cost + num_tiles + 1000 * num_turns
                new_loc_facing = loc_facing
                new_num_tiles = num_tiles
            elif node.loc_facing.loc != pred:
                new_cost = node.cost + 1000
                new_loc_facing = (node.loc_facing.loc, facing)
                new_num_tiles = 1
            else:
                continue
            if new_loc_facing in visited and visited[new_loc_facing].cost < new_cost:
                continue
            active.push((
                new_cost, new_num_tiles,
                new_loc_facing, some(node.loc_facing),
            ))
    case p1
    of Some(@p): return (p, count_tiles(visited, ends))
    of None(): return (0, 0)

var
    (graph, start, goal) = parse("input.txt")
    (p1, p2) = solve(graph, start, goal)
echo &"{p1}\n{p2}"
