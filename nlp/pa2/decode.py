# Run 'python count_cfg_freq.py [parse_train.dat | parse_train_vert.dat]' to train the model.
# The model will be written to STDOUT, so you need to redirect it to some file.
# A file called 'word_count' will also be generated in the training process.
# After that, run 'python decode.py counts test_data' to decode data using model file(counts).

# There's two pitfalls for task 2:
# 1. You can't iterate through all non-terminal terms in DP since that will
#    take O(n^3 * m^3) time. Where n is sentence length and m is number of non-terminal
#    words. Instead, iterate all the binary rules, which is far less than O(m^3).
# 2. There's sentences in the data than contains '\'. It should be escaped as '\\' or the 
#    JSON file output will be wrong

# The answer provided by the TA will give different answser from this solution.
# I've verified when they give different parsing result, the score is always the
# same. So both parsing tree are optimal and have identical score per Python's precision
# for floating point value.

import sys, json
from collections import defaultdict

class Decoder:
    def __init__(self, model_file_path, word_count_file_path):
        self.word_count = defaultdict(int)
        self.rule_count = defaultdict(int)
        self.non_terminals = set()
        self.binary_rules = set()

        with open(word_count_file_path) as wc_file:
            line = wc_file.readline()
            while line:
                line = line.strip()
                word, count = line.split()
                self.word_count[word] = int(count)
                line = wc_file.readline()

            
        with open(model_file_path) as model_file:
            line = model_file.readline()
            while line:
                line = line.strip()
                line = tuple(line.split())
                count = int(line[0])
                self.rule_count[line[2:]] = count
                if len(line) == 3:
                    self.non_terminals.add(line[2])
                elif len(line) == 5:
                    self.binary_rules.add(line[2:])
                line = model_file.readline()

    def q(self, *argv):
        rule = tuple(argv)
        base = rule[0:1]
        return float(self.rule_count[rule]) / float(self.rule_count[base])

    def handle_rare(self, word):
        return '_RARE_' if self.word_count[word] < 5 else word


    def decode(self, sentence):
        best_score = defaultdict(int)
        split = {}
        n = len(sentence)

        for idx in range(n):
            word = self.handle_rare(sentence[idx])
            for term in self.non_terminals:
                best_score[(idx, 1, term)] = self.q(term, word)

        for l in xrange(2, n + 1):
            for idx in xrange(n):
                if idx + l > n:
                    continue
                for rule in self.binary_rules:
                    term, a, b = rule
                    key = (idx, l, term)
                    score = 0.0
                    sp = None
                    p = self.q(term, a, b)
                    for mid in xrange(idx + 1, idx + l):
                        pa = best_score[(idx, mid - idx, a)]
                        pb = best_score[(mid, l - (mid - idx), b)]
                        cur = p * pa * pb
                        if cur > score:
                            score = cur
                            sp = (a, b, mid)
                    if score > best_score[key]:
                        best_score[key] = score
                        split[key] = sp

        return self.annotate(split, sentence, 0, n, 'SBARQ')

    def annotate(self, split, sentence, idx, length, term):
        if length == 1:
            return '["%s", "%s"]' % (term, sentence[idx].replace('\\', '\\\\'))
        
        a, b, mid = split[(idx, length, term)]
        
        left = self.annotate(split, sentence, idx, mid - idx, a)
        right = self.annotate(split, sentence, mid, length - (mid - idx), b)

        return '["%s", %s, %s]' % (term, left, right)

def get_sentence(path):
    with open(path) as input_file:
        line = input_file.readline()
        while line:
            line = line.strip()
            yield line.split()
            line = input_file.readline()

if __name__ == "__main__":
    decoder = Decoder(sys.argv[1], 'word_count')
    data_path = sys.argv[2]
    for sentence in get_sentence(data_path):
        print decoder.decode(sentence)
