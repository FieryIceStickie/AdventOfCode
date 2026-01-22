module Main

import System.File
import Data.Vect
import Data.List
import Data.List1
import Data.String
import Data.IOArray

chomp : File -> List String -> IO (Either FileError (List String))
chomp file ls = do
  res <- fGetLine file
  case res of
       Left err => pure (Left err)
       Right line =>
          if line == "" 
             then do
               pure $ Right (reverse ls)
             else do
               chomp file (line :: ls)

Point : Type 
Point = (Int, Int, Int)

parseInt : String -> Int
parseInt s = case parseInteger s of
                  Just n => n
                  Nothing => 0

parseLine : String -> Point
parseLine line = 
  case map parseInt $ forget (split (== ',') line) of
       [x, y, z] => (x, y, z)
       _ => (-69, -69, -69)

parse : File -> IO (Either FileError (List Point))
parse file = do
  Right lines <- chomp file Nil
    | Left err => pure (Left err)
  pure $ Right (map parseLine lines)

getPairs : List a -> List (a, a)
getPairs [] = []
getPairs (p :: ps) = map (\q => (p, q)) ps ++ getPairs ps

square : Int -> Int
square x = x * x

dist : Point -> Point -> Int
dist (x1, y1, z1) (x2, y2, z2) = (square (x1 - x2)) + (square (y1 - y2)) + (square (z1 - z2))

DSU : Type
DSU = IOArray (Int, Int)

fillDSU : Int -> DSU -> Int -> IO ()
fillDSU n dsu k =
  if n == k
     then pure ()
     else do
       _ <- writeArray dsu k (k, 1)
       fillDSU n dsu (k + 1)

makeDSU : Nat -> IO DSU
makeDSU n = do
  dsu <- newArray (cast n)
  fillDSU (cast n) dsu 0
  pure dsu

findSet : DSU -> Int -> IO Int
findSet dsu x = do
  Just (y, s) <- readArray dsu x
    | Nothing => pure 69420
  if x == y
     then pure x
     else do
       a <- findSet dsu y
       _ <- writeArray dsu x (a, s)
       pure a

merge : DSU -> Int -> Int -> IO ()
merge dsu x y = do
  Just (x', s) <- readArray dsu x
    | Nothing => pure ()
  Just (y', s') <- readArray dsu y
    | Nothing => pure ()
  _ <- writeArray dsu x (y, s)
  _ <- writeArray dsu y (y, s + s')
  pure ()

union : DSU -> Int -> Int -> IO ()
union dsu x y = do
  a <- findSet dsu x
  b <- findSet dsu y
  if a == b
     then pure ()
     else if a < b
     then merge dsu a b
     else merge dsu b a

finToInt : Fin n -> Int
finToInt n = cast (finToNat n)

unionList : DSU -> List (Fin n, Fin n) -> IO ()
unionList dsu [] = pure ()
unionList dsu ((x, y) :: ps) = do
  union dsu (finToInt x) (finToInt y)
  unionList dsu ps

unionRest : DSU -> Int -> List (Fin n, Fin n) -> IO (Maybe (Fin n, Fin n))
unionRest dsu n [] = pure Nothing
unionRest dsu n ((x, y) :: ps) = do
  let x' = finToInt x
  let y' = finToInt y
  union dsu x' y'
  a <- findSet dsu x' 
  Just (a', s) <- readArray dsu a
    | Nothing => pure Nothing
  if s == n
     then pure $ Just (x, y)
     else unionRest dsu n ps


maxThree : DSU -> Int -> Int -> Int -> Int -> Int -> IO (Int)
maxThree dsu k n a b c = do
  if k == n
     then pure (a * b * c)
     else do
       Just (x, s) <- readArray dsu k
         | Nothing => pure 69420
       if x == k then
          if s > a then 
             if s > b then
                if s > c then 
                       maxThree dsu (k+1) n b c s
                else maxThree dsu (k+1) n b s c
             else maxThree dsu (k+1) n s b c
          else maxThree dsu (k+1) n a b c
        else maxThree dsu (k+1) n a b c

main : IO ()
main = do
  Right file <- openFile "input.txt" Read
    | Left err => putStrLn ("joever" ++ show err)
  Right lpoints <- parse file
    | Left err => putStrLn ("joever" ++ show err)
  closeFile file

  let points = Data.Vect.fromList lpoints
  let pairs = getPairs $ allFins (length lpoints)
  let spairs = sortBy (\(x1, y1), (x2, y2) => compare 
                  (dist (index x1 points) (index y1 points)) 
                  (dist (index x2 points) (index y2 points))) pairs
  dsu <- makeDSU (length lpoints)

  unionList dsu (Data.List.take 1000 spairs)
  let spairs = Data.List.drop 1000 spairs
  let n = cast (length lpoints)
  p1 <- maxThree dsu 0 n 0 0 0
  Just (x, y) <- unionRest dsu (cast n) spairs
    | Nothing => putStrLn "joever 2"
  let (x1, _, _) = index x points
  let (x2, _, _) = index y points
  let p2 = x1 * x2
  putStrLn $ show p1 ++ " " ++ show p2

