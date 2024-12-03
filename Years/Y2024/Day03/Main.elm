module Y2024.Day03.Main exposing (output)

import List exposing (map)
import Regex exposing (Match)
import String exposing (fromInt, toInt)

type Toggle = Do | Dont | Mul

type alias MatchResult =
    { isDo : Toggle
    , value : Int
    }

instructionPattern : Regex.Regex
instructionPattern =
    Maybe.withDefault Regex.never <| Regex.fromString "mul\\((\\d+),(\\d+)\\)|(do)\\(\\)|(don't)\\(\\)"


getMatches : String -> List MatchResult
getMatches data = map parseMatch (Regex.find instructionPattern data) |> map (Maybe.withDefault (MatchResult Mul 0) )


safeToInt : String -> Int
safeToInt num = toInt num |> Maybe.withDefault 0


parseMatch : Match -> Maybe MatchResult
parseMatch match = 
    case match.submatches of
        [Nothing, Nothing, Just _, Nothing] -> Just { isDo = Do, value = 0 }
        [Nothing, Nothing, Nothing, Just _] -> Just { isDo = Dont, value = 0 }
        [Just x, Just y, Nothing, Nothing] -> Just { isDo = Mul, value = safeToInt x * safeToInt y }
        _ -> Nothing

type alias Vector2 =
    { x : Int
    , y : Int
    }

addVec : Vector2 -> Vector2 -> Vector2
addVec v1 v2 = { x = v1.x + v2.x, y = v1.y + v2.y }

solve : String -> Vector2
solve data = compute (getMatches data) True

compute : List MatchResult -> Bool -> Vector2
compute matches enabled =
    case matches of
        [] -> { x = 0, y = 0 }
        m::ms -> addVec (getDelta enabled m.value ) (compute ms (switchEnabled m.isDo enabled))

getDelta : Bool -> Int -> Vector2
getDelta enabled val = { x = val, y = if enabled then val else 0 }
    

switchEnabled : Toggle -> Bool -> Bool
switchEnabled isDo enabled =
    case isDo of
        Mul -> enabled
        Dont -> False
        Do -> True


output : String -> String
output data =
    let
        res =
            solve data
    in
    fromInt res.x ++ ", " ++ fromInt res.y
