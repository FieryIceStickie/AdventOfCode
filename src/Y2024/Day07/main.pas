{$MODE delphi}
program main;
uses Classes, SysUtils, StrUtils;

type
    TEquation = record
        target : int64;
        nums : array of int64;
    end;

var
    inputFile: TextFile;
    line: String;
    eqn: TEquation;
    equations: array of TEquation;
    i: Integer;
    p: Boolean;
    p1: int64;
    p2: int64;
procedure parse(const line: string; var eqn : TEquation);
var
    parts: TStringList;
    i: Integer;
begin
    parts := TStringList.Create;
    try
        parts.Delimiter := ' ';
        parts.StrictDelimiter := True;
        parts.DelimitedText := line;
        eqn.target := strToInt64(copy(parts[0], 1, length(parts[0]) - 1));
        SetLength(eqn.nums, parts.Count - 1);
        for i := 1 to parts.Count - 1 do
        begin
            eqn.nums[i - 1] := StrToInt64(parts[i]);
        end;
    finally
        parts.Free;
    end;
end;

procedure check_solvable_a(const eqn: TEquation; var p : boolean);
    function solve(const idx: int64; const num: int64) : boolean;
    var
        v: int64;
    begin
        if idx = length(eqn.nums) then
            begin;
            solve := num = eqn.target;
            exit;
            end
        else if num > eqn.target then
            begin;
            solve := false;
            exit;
            end;
        v := eqn.nums[idx];
        if solve(idx + 1, num + v) then
            begin
            solve := true;
            exit;
            end
        else if solve(idx + 1, num * v) then
            begin
            solve := true;
            exit;
            end;
        solve := false;
    end;
begin
    p := solve(1, eqn.nums[0]);
end;

procedure check_solvable_b(const eqn: TEquation; var p : boolean);
    function solve(const idx: int64; const num: int64) : boolean;
    var
        v: int64;
    begin
        if idx = length(eqn.nums) then
            begin;
            solve := num = eqn.target;
            exit;
            end
        else if num > eqn.target then
            begin;
            solve := false;
            exit;
            end;
        v := eqn.nums[idx];
        if solve(idx + 1, num + v) then
            begin
            solve := true;
            exit;
            end
        else if solve(idx + 1, num * v) then
            begin
            solve := true;
            exit;
            end
        else if solve(idx + 1, StrToInt64(IntToStr(num) + IntToStr(v))) then
            begin
            solve := true;
            exit;
            end;
        solve := false;
    end;
begin
    p := solve(1, eqn.nums[0]);
end;

begin
    AssignFile(inputFile, 'input.txt');
    Reset(inputFile);
    SetLength(equations, 0);
    while not Eof(inputFile) do
    begin
        ReadLn(inputFile, line);
        parse(line, eqn);
        SetLength(equations, Length(equations) + 1);
        equations[High(equations)] := eqn;
    end;
    CloseFile(inputFile);

    p1 := 0;
    p2 := 0;
    for i := 0 to High(equations) do
    // for i := 6 to 6 do
        begin
        p := False;
        eqn := equations[i];
        check_solvable_a(eqn, p);
        if p then
            begin
            p1 += eqn.target;
            p2 += eqn.target;
            continue;
            end;
        check_solvable_b(eqn, p);
        if p then
            begin
            p2 += eqn.target;
            end;
        end;
    writeln(p1, ' ', p2);
end.
