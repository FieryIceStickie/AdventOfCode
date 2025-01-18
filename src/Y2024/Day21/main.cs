using System;
using System.Collections.Generic;
using System.IO;
using System.Numerics;

static var keypad = new Dictionary<char, Complex> {
    {'7', new Complex(-3, -2)},
    {'8', new Complex(-3, -1)},
    {'9', new Complex(-3, 0)},
    {'4', new Complex(-2, -2)},
    {'5', new Complex(-2, -1)},
    {'6', new Complex(-2, 0)},
    {'1', new Complex(-1, -2)},
    {'2', new Complex(-1, -1)},
    {'3', new Complex(-1, 0)},
    {'0', new Complex(0, -1)},
    {'A', new Complex(0, 0)},
    {'^', new Complex(0, -1)},
    {'<', new Complex(1, -2)},
    {'v', new Complex(1, -1)},
    {'>', new Complex(1, 0)},
};

static (List<Complex>, int)[] parse(string filename) {
    string[] lines = File.ReadAllLines(filename);
    var rtn = new (List<Complex>, int)[lines.Length];
    for (int i = 0; i < lines.Length; i++) {
        string line = lines[i];
        var seq = new List<Complex> {keypad['A']};
        foreach (var c in line) {
            seq.Add(keypad[c]);
        }
        int num;
        int.TryParse(line.TrimEnd('A'), out num);
        rtn[i] = (seq, num); 
    }
    return rtn;
}

static var paths_cache = new Dictionary<(Complex, Complex), List<List<Complex>>>();
static var d_dict = new Dictionary<Complex, Complex> {
    {new Complex(-1, 0), new Complex(0, -1)},
    {new Complex(0, 1), new Complex(1, 0)},
    {new Complex(1, 0), new Complex(1, -1)},
    {new Complex(0, -1), new Complex(1, -2)},
};

static List<List<Complex>> find_all_paths(Complex start, Complex end) {
    if (paths_cache.ContainsKey((start, end))) {
        return paths_cache[(start, end)];
    }
    var paths = new List<List<Complex>>();
    void search(Complex z, List<Complex> path) {
        if (z == new Complex(0, -2)) {return;}
        if (z == end) {
            paths.Add(path.ToList());
            return;
        }
        Complex d = end - z;
        if (d.Real != 0) {
            Complex delta = new Complex(double.Sign(d.Real), 0);
            path.Add(d_dict[delta]);
            search(z + delta, path);
            path.RemoveAt(path.Count - 1);
        }
        if (d.Imaginary != 0) {
            Complex delta = new Complex(0, double.Sign(d.Imaginary));
            path.Add(d_dict[delta]);
            search(z + delta, path);
            path.RemoveAt(path.Count - 1);
        }
    }
    search(start, new List<Complex>());
    paths_cache[(start, end)] = paths;
    return paths;
}

static long minimize_seq(List<Complex> keys, int n, bool is_first = false) {
    if (n == 0) {return keys.Count - 1;}
    long sum = 0;
    for (int i = 0; i < keys.Count - 1; i++) {
        var start = keys[i];
        var end = keys[i + 1];
        sum += minimize_key(start, end, n - 1, is_first);
    }
    return sum;
}

static var key_cache = new Dictionary<(Complex, Complex, int), long>();

static long minimize_key(Complex start, Complex end, int n, bool is_first) {
    var triple = (start, end, n);
    if (!is_first && key_cache.ContainsKey(triple)) {
        return key_cache[triple];
    }
    long min = -1;
    foreach (var path in find_all_paths(start, end)) {
        var seq = new List<Complex> {new Complex(0, 0)};
        seq.AddRange(path);
        seq.Add(new Complex(0, 0));
        var res = minimize_seq(seq, n);
        if (min == -1 || res < min) {
            min = res;
        }
    }
    if (!is_first) {
        key_cache[triple] = min;
    }
    return min;
}

static long solve((List<Complex>, int)[] data, int num_keypads) {
    long sum = 0;
    foreach (var (seq, num) in data) {
        sum += minimize_seq(seq, num_keypads, true) * num;
    }
    return sum;
}

var data = parse("input.txt");
Console.WriteLine(solve(data, 3));
Console.WriteLine(solve(data, 26));

