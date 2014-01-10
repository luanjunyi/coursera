# The one caveat is the probability of any tagging for long sentences can be too small.
# There one sentence in the test data that will result in less than 1e-400 for the 
# best tagging. The trick is to make the inital probability 1e100 instead of 1.0.
# The solution provided by TA of this course didn't dealt with this and the solution was
# wrong for that particular case.

import sys, os, re, math
from collections import defaultdict
from reduce_rare import simple_reduce, four_class_reduce

def grab_sentence(infile):
    line = infile.readline()
    sentence = list()
    while line:
        line = line.strip()
        if line:
            sentence.append(line)
        else:
            yield sentence
            sentence = list()
        line = infile.readline()

class EM(object):
    def __init__(self, tag):
        self.total = 0
        self.count = defaultdict(int)
        self.tag = tag

class HMMTagger(object):
    def __init__(self):
        self.em_dict = dict()
        self.gram_count = defaultdict(int)
        self.tags = set()

    def build_index(self, filepath):
        self.em_dict = dict({'*': EM('*'), 'STOP': EM('STOP')})
        self.gram_count = defaultdict(int)
        self.tags = set(['*', 'STOP'])

        with open(filepath) as input:
            line = input.readline()
            while line:
                line = line.strip().split()
                if line[1] == 'WORDTAG':
                    count = int(line[0])
                    tag = line[2]
                    word = line[3]
                    em = self.em_dict.setdefault(tag, EM(tag))
                    em.count[word] = count
                    em.total += count
                    self.tags.add(tag)
                elif re.match(r"[1-3]-GRAM", line[1]):
                    count = int(line[0])
                    gram = tuple(line[2:])
                    self.gram_count[gram] += count
                else:
                    raise Exception("bad line: (%s)" % ' '.join(line))

                line = input.readline()

    def baseline_tagging(self, filepath):
        with open(filepath) as input:
            line = input.readline()
            while line:
                word = line.strip()
                if word:
                    if self.is_rare(word):
                         word = '_RARE_'
                    cur_tag = 'O'
                    for tag in self.em_dict:
                        if self.em(word, tag) > self.em(word, cur_tag):
                            cur_tag = tag
                    print '%s %s' % (line.strip(), cur_tag)
                else:
                    print ''
                line = input.readline()

    def viterbi_tagging(self, filepath, reducer):
        with open(filepath) as input:
            sentences = grab_sentence(input)
            for sentence in sentences:
                tags = self.viterbi(sentence, reducer)
                for i in xrange(len(sentence)):
                    print ' '.join([sentence[i], tags[i]])
                print ''

    def viterbi(self, words, reducer):
        n = len(words)
        rec = defaultdict(float)
        trace = defaultdict(str)
        ret = list()
        rec[-1, '*', '*'] = 1.0e100
        trace[-1, '*', '*'] = '*'
        for idx in xrange(0, n):
            word = words[idx]
            if self.is_rare(word):
                word = reducer(word)
            for cur in self.tags:
                e = self.em(word, cur)
                for b in self.tags:
                    best_score = 0.0
                    best_trace = ' '
                    for a in self.tags:
                        prob = rec[idx - 1, a, b] * self.q((a, b, cur)) * e
                        if prob > best_score:
                            best_score = prob
                            best_trace = a
                    rec[idx, b, cur] = best_score
                    trace[idx, b, cur] = best_trace

        best_score = 0.0
        best_trace = []
        for a in self.tags:
            for b in self.tags:
                prob = rec[n - 1, a, b] * self.q((a, b, 'STOP'))
                if prob > best_score:
                    best_score = prob
                    best_trace = [a, b]

        ret = best_trace
        ret.reverse()
        idx = n - 1

        while len(ret) < n:
            last = trace[idx, ret[-1], ret[-2]]
            ret.append(last)
            idx -= 1
        ret.reverse()
        return ret
    
        
    def is_rare(self, word):
        for tag in self.em_dict:
            if self.em_dict[tag].count[word] > 0:
                return False
        return True

    def em(self, x, y):
        if y in ('*', 'STOP'):
            return 0.0
        return float(self.em_dict[y].count[x]) / float(self.em_dict[y].total)

    def q(self, gram):
        try:
            return float(self.gram_count[tuple(gram)]) / float(self.gram_count[tuple(gram[:-1])])
        except Exception, err:
            return 0.0

if __name__ == "__main__":
    count_file_path = sys.argv[1]
    test_file_path = sys.argv[2]
    if len(sys.argv) > 3:
        reducer = eval(sys.argv[3])
    else:
        reducer = simple_reduce
    tagger = HMMTagger()
    tagger.build_index(count_file_path)
    tagger.viterbi_tagging(test_file_path, reducer)
