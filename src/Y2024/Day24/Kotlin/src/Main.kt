import java.io.File
import java.io.InputStream
import java.util.stream.Stream
import kotlin.reflect.typeOf


class Eqn(val op: String, val a: String, val b: String) {
    operator fun component1() = op
    operator fun component2() = a
    operator fun component3() = b
}
class ParseRtn(
    private val values: HashMap<String, Int>,
    private val eqns: Map<String, Eqn>,
    private val zCount: Int
) {
    operator fun component1(): HashMap<String, Int> {
        return values
    }

    operator fun component2(): Map<String, Eqn> {
        return eqns
    }

    operator fun component3(): Int {
        return zCount
    }
}

fun parse(filename: String): ParseRtn {
    val inputStream: InputStream = File(filename).inputStream()
    val inputString = inputStream.bufferedReader().use { it.readText() }
    val (valueStr, eqnStr) = inputString.split("\n\n")
    val values = HashMap<String, Int>()
    valueStr.split("\n").forEach {
        val (k, v) = it.split(": ")
        values[k] = v.toInt()
    }
    val eqns = HashMap<String, Eqn>()
    eqnStr.split("\n").forEach {
        val (eqn, res) = it.split(" -> ")
        val (a, op, b) = eqn.split(" ")
        eqns[res] = Eqn(op, a, b)
    }
    val zCount = values.size / 2 + 1
    return ParseRtn(values, eqns, zCount)
}

val prioDict: HashMap<String, Int> = hashMapOf(
    "XOR" to 0,
    "AND" to 1,
    "OR" to 2,
)

interface INode: Comparable<INode> {
    val name: String
    override fun compareTo(other: INode): Int {
        if (this is Str && other is Str) {
            return this.name.compareTo(other.name)
        } else if (this is Str && other is Node) {
            return -1
        } else if (this is Node && other is Str) {
            return 1
        } else if (this is Node && other is Node) {
            if (op != other.op) {
                return prioDict[op]!!.compareTo(prioDict[other.op]!!)
            }
            if (this.left is Str && other.left is Str) {
                return if (this.left.name.startsWith("x")) -1 else 1
            }
            return this.left.compareTo(other.left)
        }
        throw IllegalArgumentException("bruh")
    }
}

class Node (override val name: String, val op: String, val left: INode, val right: INode, val res: Int): INode {
    override fun toString(): String {
        return "($name: $left $op $right)"
    }
}

class Str (override val name: String): INode {
    override fun toString(): String {
        return name
    }
}

fun pad(z: Int): String {
    return z.toString().padStart(2, '0')
}


fun matcher(tree: Node, z: Int, jumper: HashSet<String>): String? {
    if (z < 3 || z == 45) return null
    if (tree.op != "XOR") return tree.name
    val l = tree.left
    if (l is Node) {
        if (l.op != "XOR") return l.name
        if (l.left is Str && l.right is Str) {
            if (l.left.name != "x" + pad(z) || l.right.name != "y" + pad(z)) {
                return l.name
            }
        }
    }
    val r = tree.right
    if (r is Node) {
        if (r.op != "OR") return r.name
        val (rl, rr) = Pair(r.left, r.right)
        if (rl is Node) {
            if (rl.op != "AND"
                || rl.left.name != "x" + pad(z - 1)
                || rl.right.name != "y" + pad(z - 1)) {
                return rl.name
            }
        }
        if (rr is Node) {
            if (rr.op != "AND" || hashSetOf(rr.left.name, rr.right.name) != jumper ) {
                return rr.name
            }
        }
    }
    return null
}

fun solve(data: ParseRtn): Pair<Long, String> {
    val (values, eqns, zCount) = data
    val swaps = HashSet<String>()
    var jumper = HashSet<String>()

    fun traverse(node: String): INode {
        if (node in jumper || node !in eqns.keys) {
            return Str(node)
        }
        val (op, a, b) = eqns[node]!!
        var (anode, bnode) = Pair(traverse(a), traverse(b))
        if (bnode < anode) {
            anode = bnode.also { bnode = anode }
        }
        val av = values[anode.name]!!
        val bv = values[bnode.name]!!
        val res = when (op) {
            "XOR" -> av xor bv
            "AND" -> av and bv
            "OR" -> av or bv
            else -> throw IllegalArgumentException("foobar")
        }
        values[node] = res
        return Node(node, op, anode, bnode, res)
    }

    for (z in 0..<zCount) {
        val tree = traverse("z" + pad(z))
        if (tree !is Node) {
            throw IllegalArgumentException("tree")
        }
        val res = matcher(tree, z, jumper)
        if (res != null) {
            swaps.add(res)
        }
        jumper = hashSetOf(
            tree.left.name,
            tree.right.name,
        )
    }
    return Pair(
        (0..<zCount)
            .map { values["z" + pad(it)]!! }
            .joinToString("")
            .reversed()
            .toLong(2),
        swaps.sorted().joinToString(","),
    )
}


fun main() {
    val data = parse("../input.txt")
    val (p1, p2) = solve(data)
    println(p1)
    println(p2)
}
