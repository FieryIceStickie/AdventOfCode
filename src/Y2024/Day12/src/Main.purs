module Main where

import Prelude

import Data.Array (length, range)
import Data.Complex (Cartesian(..), imag, real)
import Data.Foldable (foldl, foldr, sum)
import Data.FoldableWithIndex (foldlWithIndex)
import Data.FunctorWithIndex (mapWithIndex)
import Data.HashMap as Map
import Data.HashSet as Set
import Data.Hashable (class Hashable, hash)
import Data.Maybe (Maybe(..), fromMaybe)
import Data.Newtype (class Newtype, unwrap)
import Data.String (Pattern(..), split)
import Data.Tuple (Tuple(..), fst, snd)
import Effect (Effect)
import Effect.Console (logShow)
import Node.Encoding (Encoding(..))
import Node.FS.Sync (readTextFile)

newtype Complex = Complex (Cartesian Int)

derive instance Newtype Complex _
derive newtype instance Eq Complex
derive newtype instance Show Complex
derive newtype instance Semiring Complex
derive newtype instance Ring Complex

c :: Int -> Int -> Complex
c a b = Complex (Cartesian a b)

instance Hashable Complex where
    hash p = let z = unwrap p in Tuple (real z) (imag z) # hash

newtype Node = Node
    { parent :: Complex
    , plant :: String
    , size :: Int
    }

derive instance Newtype Node _

instance Show Node where
    show a = do
        let n = unwrap a
        "{parent: "
            <> show (unwrap n.parent)
            <> ", plant: "
            <> n.plant
            <> ", size: "
            <> show n.size
            <> "}"

zero :: Complex
zero = c 0 0

i :: Complex
i = c 0 1

one :: Complex
one = c 1 0

def_node :: Node
def_node = Node { parent: zero, plant: "", size: 0 }

get :: forall k v. Hashable k => v -> k -> Map.HashMap k v -> v
get d k = Map.lookup k >>> fromMaybe d

find_set :: DSU -> Complex -> Tuple Complex DSU
find_set dsu z = do
    let k = (unwrap $ get def_node z dsu).parent
    if k == z then Tuple z dsu
    else do
        let res = find_set dsu k
        Tuple (fst res) (Map.update (change_parent (fst res) >>> pure) z (snd res))

change_parent :: Complex -> Node -> Node
change_parent parent node = do
    let n = unwrap node
    Node { parent: parent, plant: n.plant, size: n.size }

type DSU = Map.HashMap Complex Node

make_set_inner :: DSU -> Complex -> Complex -> Maybe DSU
make_set_inner dsu z1 z2 = do
    let res1 = find_set dsu z1
    let a = fst res1
    let res2 = find_set (snd res1) z2
    let b = fst res2
    let t = snd res2
    if a == b then t # Just
    else
        ( do
              an <- Map.lookup a t
              bn <- Map.lookup b t
              if (unwrap an).size < (unwrap bn).size then t # Map.insertWith seme a bn # Map.insertWith uke b an # Just
              else t # Map.insertWith uke a bn # Map.insertWith seme b an # Just
        )

make_set :: DSU -> Complex -> Complex -> DSU
make_set dsu z1 = make_set_inner dsu z1 >>> fromMaybe Map.empty

seme :: Node -> Node -> Node
seme self other = do
    let s = unwrap self
    let o = unwrap other
    Node { parent: o.parent, plant: s.plant, size: s.size }

uke :: Node -> Node -> Node
uke self other = do
    let s = unwrap self
    let o = unwrap other
    Node { parent: s.parent, plant: s.plant, size: s.size + o.size }

parse :: Array String -> DSU
parse = mapWithIndex parse_row >>> foldl Map.union Map.empty

parse_row :: Int -> String -> DSU
parse_row x row = split (Pattern "") row
    # foldlWithIndex
          ( \y dsu s -> do
                let z = c x y
                Map.insert z (Node { parent: z, plant: s, size: 1 }) dsu
          )
          Map.empty

fill_dsu :: Int -> DSU -> DSU
fill_dsu size dsu = foldl
    ( \d0 d ->
          foldl
              ( \d1 x ->
                    foldl
                        ( \d2 y -> combine_dsu d (c x y) d2
                        )
                        d1 $ range 0 (size - 1)
              )
              d0 $ range 0 (size - 1)
    )
    dsu
    [ c 1 0, c 0 1 ]

combine_dsu :: Complex -> Complex -> DSU -> DSU
combine_dsu d z dsu =
    let
        loc = z + d
        loc_node = unwrap $ get def_node loc dsu
        z_node = unwrap $ get def_node z dsu
    in
        if Map.member loc dsu && loc_node.plant == z_node.plant then make_set dsu z loc
        else dsu

type Edge = Tuple Complex Complex
type CSet = Set.HashSet Edge

xor :: forall a. Hashable a => Set.HashSet a -> Set.HashSet a -> Set.HashSet a
xor a b = Set.difference (Set.union a b) (Set.intersection a b)

optimize_dsu :: DSU -> DSU
optimize_dsu dsu = foldl (\d -> find_set d >>> snd) dsu $ Map.keys dsu

neighbourhood :: Complex -> CSet
neighbourhood z = Set.fromArray [ Tuple i zero, Tuple i one, Tuple one zero, Tuple one i ]
    # Set.map (\tup -> Tuple (fst tup) (snd tup + z))

get_edges :: DSU -> Map.HashMap Complex CSet
get_edges dsu = Map.keys dsu
    # foldr
          ( \k -> do
                let edges = neighbourhood k
                Map.upsert (xor $ edges) (find_set dsu k # fst) edges
          )
          Map.empty

get_size :: Complex -> DSU -> Int
get_size z dsu = case Map.lookup z dsu of
    Just node -> unwrap node # _.size
    Nothing -> 0

calc :: (CSet -> Int) -> DSU -> Map.HashMap Complex CSet -> Int
calc f dsu edges =
    Map.toArrayBy
        ( \z s ->
              (get_size z dsu) * (f s)
        )
        edges # sum

count_cannons :: CSet -> Int
count_cannons s = s
    # Set.filter
          ( \m -> do
                let edge = fst m
                let pos = snd m
                let alt_edge = one + i - edge
                not $ Set.member (Tuple edge (pos - edge)) s && Set.isEmpty (Set.intersection s $ Set.fromArray [Tuple alt_edge pos, Tuple alt_edge (pos - alt_edge)])
          )
    # Set.size

main :: Effect Unit
main = do
    lines <- split (Pattern "\n") <$> readTextFile UTF8 "input.txt"
    let size = length lines
    let dsu = optimize_dsu $ parse lines # fill_dsu size
    let edges = get_edges dsu
    let p1 = calc Set.size dsu edges
    let p2 = calc count_cannons dsu edges
    logShow p1
    logShow p2
