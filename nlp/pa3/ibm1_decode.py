import os, sys
import cPickle as pickle

from ibm1_train import load_corpus

def argmax(ls):
    if not ls:
        return None, 0.0
    return max(ls, key = lambda x: x[1])

class IBM1(object):
    def __init__(self, modelfile):
        model = pickle.load(modelfile)
        self.t = model.c

    def get_t(self, f, e):
        if e not in self.t or (f, e) not in self.t:
            return 0.0
        return self.t[f, e] / self.t[e]

    def decode_file(self, from_lang_path, to_lang_path):
        self.from_corpus = load_corpus(from_lang_path)
        self.to_corpus = load_corpus(to_lang_path)
        for e_sent in self.to_corpus:
            e_sent.insert(0, 'NULL')
        size = len(self.from_corpus)
        for k in xrange(size):
            f_sent = self.from_corpus[k]
            e_sent = self.to_corpus[k]
            for i, f in enumerate(f_sent):
                j, _ = argmax([(j, self.get_t(f, e)
                                ) for j, e in enumerate(e_sent)])
                print "%d %d %d" % (k + 1, j, i + 1)


if __name__ == "__main__":
    ibm = IBM1(open("ibm1.model", "r"))
    from_lang_path = sys.argv[1]
    to_lang_path = sys.argv[2]
    ibm.decode_file(from_lang_path, to_lang_path)
