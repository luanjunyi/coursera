import os, sys
from collections import defaultdict
import cPickle as pickle
from ibm1_train import load_corpus, IBM1


class IBM2(object):
    def __init__(self, from_lang_file, to_lange_file):
        self.from_lang_file = from_lang_file
        self.to_lange_file = to_lange_file

    def delta(self, k, i, j):
        return self.prob(k, i, j) / self.prob_sum(k, i)

    def prob(self, k, i, j):
        f = self.from_corpus[k][i]
        e = self.to_corpus[k][j]
        m = len(self.from_corpus[k])
        l = len(self.to_corpus[k])
        return self.q(i, j, m, l) * self.t(f, e)

    def q(self, i, j, m, l):
        return self.c.get((i, j, m, l), 0.0) / self.c[j, m, l] if (not self.first_run) else 1.0 / l

    def t(self, f, e):
        return self.c.get((f, e), 0.0) / self.c.get(e, 0.0)

    def prob_sum(self, k, i):
        ret = 0.0
        l = len(self.to_corpus[k])
        for j in range(l):
            ret += self.prob(k, i, j)
        return ret

    def train(self, ibm1_model_path):
        with open(ibm1_model_path, "r") as model_file:
            ibm1 = pickle.load(model_file)
            self.c = ibm1.c
        print 'training IBM model two'
        self.from_corpus = load_corpus(self.from_lang_file)
        self.to_corpus = load_corpus(self.to_lange_file)
        for e_sent in self.to_corpus:
            e_sent.insert(0, 'NULL')
        
        for count in range(5):
            self.first_run = (count == 0)
            cur_c = dict()
            for idx, f_sent in enumerate(self.from_corpus):
                if idx % 200 == 0:
                    print "iteration %d - %d processed" % (count+1, idx)
                t_sent = self.to_corpus[idx]
                m = len(f_sent)
                l = len(t_sent)
                for i,f in enumerate(f_sent):
                    total = self.prob_sum(idx, i)
                    for j,e in enumerate(t_sent):
                        d = self.prob(idx, i, j) / total
                        cur_c.setdefault(e, 0.0)
                        cur_c[e] += d
                        cur_c.setdefault((f, e), 0.0)
                        cur_c[f, e] += d
                        cur_c.setdefault((i, j, m, l), 0.0)
                        cur_c[i,j,m,l] += d
                        cur_c.setdefault((j, m, l), 0.0)
                        cur_c[j,m,l] += d
            self.c = cur_c
        

if __name__ == "__main__":
    ibm2 = IBM2("corpus.es", "corpus.en")
    ibm2.train("imb1.model")
    with open("ibm2.model", "w") as outfile:
        pickle.dump(ibm2, outfile)
