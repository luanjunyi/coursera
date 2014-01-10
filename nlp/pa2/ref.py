from __future__ import division
import sys, json


class PCFG:
    "Store the counts from a corpus."
    def __init__(self, nonterms, bin_rules, unary_rules, words):
        "Initialize the PCFG."
        self.nonterms = dict(nonterms)
        self.bin_rules = dict(bin_rules)
        self.unary_rules = dict(unary_rules)
        self.words = words
        # Set up binary rule table.
        self.bin_rule_table = {}
        for (a, b, c), count in bin_rules:
            self.bin_rule_table.setdefault(a, [])
            self.bin_rule_table[a].append((b, c))


    def has_unary_rule(self, nonterm, word):
        "Does the grammar have this unary rule?"
        return (nonterm, word) in self.unary_rules

    def nonterminals(self):
        "Returns the list of nonterminals."
        return self.nonterms.keys()
    
    def rules(self, a):
        "Returns all the binary rules of the form a -> b c."
        return [(a, b, c) for b, c in self.bin_rule_table.get(a, [])]

    def binary_rule_prob(self, rule):
        "Probability of a binary rule."
        return self.bin_rules[rule] / self.nonterms[rule[0]]

    def unary_rule_prob(self, rule):
        "Probability of a unary rule."
        return self.unary_rules[rule] / self.nonterms[rule[0]]

    def is_rare_word(self, word):
        "Is a word rare in this PCFG."
        return self.words.get(word, 0) < 5

    @staticmethod
    def from_handle(handle):
        "Read the rules from a file handle."
        nonterms = []
        bin_rules = []
        unary_rules = []
        words = {}
        for l in handle:
            t = l.strip().split()
            count = float(t[0])
            if t[1] == "NONTERMINAL":
                nonterms.append((t[2], count))
            if t[1] == "BINARYRULE":
                bin_rules.append(((t[2], t[3], t[4]), count))
            if t[1] == "UNARYRULE":
                unary_rules.append(((t[2], t[3]), count))
                words.setdefault(t[3], 0)
                words[t[3]] += count
        return PCFG(nonterms, bin_rules, unary_rules, words)

def replace_rare_words(pcfg, tree):
    "Mutate tree to replace rare words."
    if len(tree) == 3:
        replace_rare_words(pcfg, tree[1])
        replace_rare_words(pcfg, tree[2])
    elif len(tree) == 2:
        if pcfg.is_rare_word(tree[1]): tree[1] = "_RARE_"

def argmax(ls):
    "Compute the argmax of a list (item, score) pairs."
    if not ls: return None, 0.0
    return max(ls, key = lambda x: x[1])

def CKY(pcfg, sentence):
    "Run the CKY algorithm."
    # Define variables to have the same names as notes.
    n = len(sentence)
    N = pcfg.nonterminals()
    x = ["" ]+ replace_rare_sent(pcfg, sentence)
    def q1(X, Y): return pcfg.unary_rule_prob((X, Y))
    def q2(X, Y, Z): return pcfg.binary_rule_prob((X, Y, Z))
    pi = {}
    bp = {}
    # Initialize the chart.
    for i in range(1, n + 1):
        for X in N:
            if pcfg.has_unary_rule(X, x[i]):
                pi[i, i, X] = q1(X, x[i])
                bp[i, i, X] = (X, sentence[i-1], i, i)

    # Dynamic program.
    for l in range(1, n):
        for i in range(1, n - l + 1):
            j = i + l
            for X in N:
                # Note that we only check rules that exist in training
                # and have non-zero probability.
                back, score = argmax([((X, Y, Z, i, s, j),
                                       q2(X, Y, Z) * pi[i, s, Y] * pi[s + 1, j, Z])
                                      for s in range(i, j)
                                      for X, Y, Z in pcfg.rules(X)
                                      if pi.get((i, s, Y), 0.0) > 0.0
                                      if pi.get((s + 1, j, Z), 0.0) > 0.0
                                      ])
                if score > 0.0: bp[i, j, X], pi[i, j, X] = back, score

     # Return the tree root'd in SBARQ.
    if (1, n, "SBARQ") in pi:
        tree = backtrace(bp[1, n, "SBARQ"], bp)
        return tree, pi[(1, n, "SBARQ")]

def backtrace(back, bp):
    "Extract the tree from the backpointers."
    if not back: return None
    if len(back) == 6:
        (X, Y, Z, i, s, j) = back
        return [X, backtrace(bp[i, s, Y], bp),
                backtrace(bp[s + 1, j, Z], bp)]
    else:
        (X, Y, i, i) = back
        return [X, Y]


def replace_rare_sent(pcfg, sent):
    "Replace rare words in a flat sentence."
    return [word if not pcfg.is_rare_word(word) else "_RARE_" for word in sent]

def main(mode, count_file, sentence_file):
    pcfg = PCFG.from_handle(open(count_file))
    for i,l in enumerate(open(sentence_file)):
        if mode == "PARSE":
            sentence = l.strip().split()
            parse, score = CKY(pcfg, sentence)
            print score, json.dumps(parse)
        elif mode == "REPLACE":
            parse = json.loads(l.strip())
            replace_rare_words(pcfg, parse)
            print json.dumps(parse)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
