import os, sys
import cPickle as pickle

from ibm1_train import load_corpus
from ibm2_train import IBM2

def argmax(ls):
    if not ls:
        return None, 0.0
    return max(ls, key = lambda x: x[1])

class IBM2Decode(IBM2):
    def __init__(self, modelfile):
        model = pickle.load(modelfile)
        self.c = model.c
        self.first_run = False

    def get_alignment(self, k):
        f_sent = self.from_corpus[k]
        e_sent = self.to_corpus[k]
        ret = list()
        for i, f in enumerate(f_sent):
            j, _ = argmax([(j, self.prob(k, i, j)) for j, e in enumerate(e_sent)])
            ret.append(j)
        return ret

    def load_file(self, from_lang_path, to_lang_path):
        self.from_corpus = load_corpus(from_lang_path)
        self.to_corpus = load_corpus(to_lang_path)
        for e_sent in self.to_corpus:
            e_sent.insert(0, 'NULL')

    def decode_file(self, from_lang_path, to_lang_path):
        self.load_file(from_lang_path, to_lang_path)

        size = len(self.from_corpus)
        for k in xrange(size):
            align = self.get_alignment(k)
            for i, j in enumerate(align, 1):
                print "%d %d %d" % (k + 1, j, i)

    def size(self):
        assert len(self.from_corpus) == len(self.to_corpus)
        return len(self.from_corpus)


if __name__ == "__main__":
    ibm = IBM2Decode(open("ibm2.model", "r"))
    from_lang_path = sys.argv[1]
    to_lang_path = sys.argv[2]
    ibm.decode_file(from_lang_path, to_lang_path)
