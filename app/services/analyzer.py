from collections import defaultdict

def analyze_file(file_path: str) -> dict:
    total_stat = defaultdict(int)
    line_stat = defaultdict(list)
    sign_dict = ["?", ".", ",", "!"]

    with open(file_path, "r", encoding="utf-8") as f:
        for line_indx, line in enumerate(f):
            word_count_in_line = defaultdict(int)
            for sign in sign_dict:
                line = line.replace(sign, "")
            splitted_line = line.split()
            for word in splitted_line:
                word = word.lower().strip()
                if not word: continue
                total_stat[word] += 1
                word_count_in_line[word] += 1
            for word, count in word_count_in_line.items():
                for i in range(line_indx - len(line_stat[word])):
                    line_stat[word].append(0)
                line_stat[word].append(count)
    return {
        "total": dict(total_stat),
        "per_line": dict(line_stat)
    }
