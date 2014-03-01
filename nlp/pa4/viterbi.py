import sys, os
from collections import defaultdict
from util import *
from feat import feat_score
from log import _logger

class Viterbi(object):
    def __init__(self, model):
        self.v = defaultdict(float)
        if model != 'EMPTY':
            self.load(model)
        else:
            self.v = None

    def load(self, model):
        with open(model) as model_file:
            for line in model_file:
                line, val = line.strip().split(' ')
                val = float(val)
                line = line.split('#')
                self.v[tuple(line)] = val

    def decode(self, filepath):
        with open(filepath) as test_file:
            sent_gen = gen_sentence(test_file)
            for sent in sent_gen:
                tags = self.decode_one(list(sent))
                assert len(tags) == len(sent)
                for token, tag in zip(sent, tags):
                    print token, tag
                print ''

    def T(self, idx, n):
        if idx <= 1:
            return ['__*__']
        elif idx == n - 1:
            return ['STOP']
        else:
            return ['O', 'I-GENE']

    def decode_one(self, sent):
        sent[:0] = ['__*__', '__*__']
        sent.append('__STOP__')
        n = len(sent)
        rec = dict()
        self.rec = rec
        bp = dict()
        rec[1, '__*__', '__*__'] = 0.0
        for i in xrange(2, n):
            for v in self.T(i, n):
                for u in self.T(i-1, n):
                    rec[i, u, v] = max([self.score(i, t, u, v, sent) for t in self.T(i-2, n)])
                    bp[i, u, v] = argmax([(t, self.score(i, t, u, v, sent)) 
                                          for t in self.T(i-2, n)])

        ret = ['STOP',]
        tag = argmax([(t, rec[n-1, t, 'STOP'])
                      for t in self.T(n-2, n)])
        ret.append(tag)

        for i in xrange(n-3, -1, -1):
            tag = bp[i+2, ret[-1], ret[-2]]
            ret.append(tag)
        ret.reverse()
        return ret[2:-1]
    
    def score(self, i, t, u, v, sent):
        return self.rec[i-1, t, u] + feat_score(i, t, u, v, sent, self.v)


if __name__ == "__main__":
    model = sys.argv[1]
    test_path = sys.argv[2]
    decoder = Viterbi(model)
    decoder.decode(test_path)
