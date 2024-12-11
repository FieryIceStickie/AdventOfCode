with Ada.Text_IO; use Ada.Text_IO; 
with Ada.Numerics; use Ada.Numerics;
with Ada.Strings.Hash;
with Ada.Containers; use Ada.Containers;
with Ada.Containers.Hashed_Sets;
with Ada.Containers.Indefinite_Hashed_Maps;
with Ada.Containers.Vectors;
with Ada.Numerics.Complex_Types; use Ada.Numerics.Complex_Types;
with Ada.Numerics.Complex_Elementary_Functions; use Ada.Numerics.Complex_Elementary_Functions;
with Ada.Text_IO.Complex_IO;

procedure main is

    package C_IO is new
        Ada.Text_IO.Complex_IO (Complex_Types);
    use C_IO;

    function Hash_Complex (z : Complex) return Ada.Containers.Hash_Type is
    begin
        return Ada.Strings.Hash (z.Re'Image) xor Ada.Strings.Hash (z.Im'Image);
    end Hash_Complex;
    function Hash_Character (c : Character) return Ada.Containers.Hash_Type is
    begin
        return Ada.Strings.Hash (c'Image);
    end Hash_Character;

    package Vector_Locs is new
        Ada.Containers.Vectors
            (Index_Type => Natural,
             Element_Type => Complex);
    use Vector_Locs;

    package Set_Locs is new
        Ada.Containers.Hashed_Sets
            (Element_Type => Complex,
             Hash => Hash_Complex,
             Equivalent_Elements => "="); 
    use Set_Locs;

    package Antenna_Locs is new
        Ada.Containers.Indefinite_Hashed_Maps 
            (Key_Type => Character,
             Element_Type => Vector,
             Hash => Hash_Character,
             Equivalent_Keys => "=");
    use Antenna_Locs;

    F : File_Type;
    File_Name : constant String := "input.txt";
    Antennas : Map;

    procedure D_Add(M: in out Map; K: Character; V: Complex) is
        Vec : Vector;
    begin
        if not M.contains(K) then
            M.include(K, Vec);
        end if;
        M(K).Append(V);
    end D_Add;

    X, Y : Integer;
    Z : Complex;

    function Within (Z : Complex) return Boolean is
        Re : Integer := Integer(Z.Re);
        Im : Integer := Integer(Z.Im);
    begin
        return 0 <= Re and Re < X and 0 <= Im and Im < Y;
    end Within;

    P1_Antinodes, P2_Antinodes : Set;
begin
    Open (F, In_File, File_Name);
    
    X := 0;
    while not End_Of_File (F) loop
        declare
            Line : String := Get_Line(F); 
        begin
            Y := 0;
            for I in Line'range loop
                if Line(I) /= '.' then
                    Z := (Float(X), Float(Y));
                    D_Add(Antennas, Line(I), Z);
                end if;
                y := y + 1;
            end loop;
        end;
        x := x + 1;
    end loop;
    Close (F);

    for Antenna in Antennas.Iterate loop
        declare
            V : Vector := Antennas(Antenna);
            Z1, Z2, D : Complex;
        begin
            for I in V.First_Index .. V.Last_Index loop
                for J in I+1 .. V.Last_Index loop
                    Z1 := V(I);
                    Z2 := V(J);
                    D := Z2 - Z1;
                    if Within(Z2 + D) then
                        P1_Antinodes.Include(Z2 + D);
                    end if;
                    if Within(Z1 - D) then
                        P1_Antinodes.Include(Z1 - D);
                    end if;
                    while Within(Z2) loop
                        P2_Antinodes.Include(Z2);
                        Z2 := Z2 + D;
                    end loop;
                    while Within(Z1) loop
                        P2_Antinodes.Include(Z1);
                        Z1 := Z1 - D;
                    end loop;
                end loop;
            end loop;
        end;
    end loop;

    Put_Line(P1_Antinodes.Length'Image & " " & P2_Antinodes.Length'Image);
end main; 
