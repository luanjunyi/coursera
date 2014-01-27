import os, sys
import cPickle as pickle

def load_corpus(filepath):
    corpus = list()
    with open(filepath) as f:
        line = f.readline()
        while line:
            line = line.strip()
            corpus.append(line.split(' '))
            line = f.readline()
    return corpus


class IBM1(object):
    def __init__(self, from_lang_file, to_lange_file):
        self.from_lang_file = from_lang_file
        self.to_lange_file = to_lange_file

    # not used for this assignment
    def delta(self, k, i, j):
        return self.t(k, i, j) / self.t_sum(k, i)

    def t(self, k, i, j):
        f = self.from_corpus[k][i]
        e = self.to_corpus[k][j]
        return float(self.c.get((f, e), 0.0)) / float(self.c.get(e, 0.0))

    def t_sum(self, k, i):
        ret = 0
        for j in range(len(self.to_corpus[k])):
            ret += self.t(k, i, j)
        return ret
            

    def train(self):
        print 'training IBM model one'
        self.from_corpus = load_corpus(self.from_lang_file)
        self.to_corpus = load_corpus(self.to_lange_file)
        for e_sent in self.to_corpus:
            e_sent.insert(0, 'NULL')
        self.c = dict()

        # Initialize n(e) for each English word as the number of 
        # foreign words ever shown up in a foreign sentence that
        # contains the English word
        for idx, f_sent in enumerate(self.from_corpus):
            t_sent = self.to_corpus[idx]
            for f in f_sent:
                for e in t_sent:
                    if (f, e) not in self.c:
                        self.c[f, e] = 1.0
                        self.c.setdefault(e, 0.0)
                        self.c[e] += 1.0
        
        for count in range(5):
            cur_c = dict()
            for idx, f_sent in enumerate(self.from_corpus):
                if idx % 200 == 0:
                    print "iteration %d - %d processed" % (count+1, idx)
                t_sent = self.to_corpus[idx]
                for i,f in enumerate(f_sent):
                    tmp = self.t_sum(idx, i)
                    for j,e in enumerate(t_sent):
                        d = self.t(idx, i, j) / tmp
                        cur_c.setdefault(e, 0.0)
                        cur_c[e] += d
                        cur_c.setdefault((f, e), 0.0)
                        cur_c[f, e] += d
            self.c = cur_c
        

if __name__ == "__main__":
    ibm = IBM1("corpus.es", "corpus.en")
    ibm.train()
    with open("ibm1.model", "w") as outfile:
        pickle.dump(ibm, outfile)
