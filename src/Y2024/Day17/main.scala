import scala.io.Source
import scala.collection.mutable.ArrayBuffer
import scala.math.BigInt
import scala.util.boundary, boundary.break

@main
def main(): Unit =
  val it = Source.fromFile("input.txt").getLines()
  var a: BigInt = it.next().drop(12).toIntOption.getOrElse(-1)
  (1 to 3) foreach (_ => it.next)
  val program: Array[BigInt] = it.next()
    .drop(9)
    .split(",")
    .map(s => s.toIntOption.getOrElse(-1))
  val ext_it = program
    .grouped(2)
    .filter(g => g(0) == 1)
    .map(g => g(1))
  val v: BigInt = ext_it.next()
  val w: BigInt = ext_it.next()

  val divideInts = (x: BigInt, y: BigInt) => (x / y, x % y)
  val f = (a: BigInt, r: BigInt) => ((r ^ v ^ w) ^ (a >> (r ^ v).toInt)) & 7

  val out = ArrayBuffer[BigInt]()
  while (a > 0) {
    val (q, r) = divideInts(a, 8)
    out += f(a, r)
    a = q
  }
  val p1 = out
    .map(_.toString)
    .mkString(",")

  def solve(n: BigInt, t: Int): BigInt = {
    boundary:
      if (t == program.length) {
        break(n)
      }
      var range = 0 to 0
      if (t == 0) {
        range = 1 to 7
      } else {
        range = 0 to 7
      }
      range foreach (r => {
        val a = (n << 3) + r
        if (f(a, r) == program(program.length - t - 1)) {
          val res = solve(a, t+1)
          if (res != 0) {
            break(res)
          }
        }
      })
      0
  }
  println(p1)
  println(solve(0, 0))
