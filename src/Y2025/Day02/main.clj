(ns Y2025.Day02.main)

(defn parse_range [res]
  (->>
   (rest res)
   (map Long/parseLong)))

(defn parse [filename]
  (->>
   (slurp filename)
   (re-seq #"(\d+)-(\d+)")
   (map parse_range)))

(defn count_pat [[a b] pat]
  (->>
   (range a (inc b))
   (filter #(->>
             (str %)
             (re-matches pat)
             nil?
             false?))
   (reduce +)))

(defn solve [ranges pat]
  (->>
   ranges
   (map #(count_pat % pat))
   (reduce +)))

(defn main []
  (->
   (parse "input.txt")
   ((juxt #(solve % #"(\d+)\1") #(solve % #"(\d+)(\1+)")))
   (println)))

(main)
