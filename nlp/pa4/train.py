import os, sys
from collections import defaultdict
from util import *
from viterbi import Viterbi
from feat import feat_vect
from log import _logger

class Perceptron(object):
    def __init__(self, train_file_path):
        self.train_file = train_file_path
        self.v = defaultdict(float)
        self.iter = 5

    def train(self, outpath):
        self.v = defaultdict(float)
        for i in xrange(self.iter):
            _logger.info("training iteration %d" % (i+1))
            self.train_iteration(self.train_file)
        with open(outpath, "w") as outfile:
            for k, v in self.v.items():
                if v == 0.0:
                    continue
                outfile.write("%s %.1f\n" % ('#'.join(k), v))

    def train_iteration(self, filepath):
        viterbi = Viterbi("EMPTY")
        viterbi.v = self.v
        with open(filepath) as train_file:
            corpus = gen_sentence_train(train_file)
            count = 0
            for doc in corpus:
                count += 1
                if count % 1000 == 0:
                    _logger.debug("%d sentence processed" % count)
                sent = [s[0] for s in doc]
                tags = [s[1] for s in doc]
                tags_pred = viterbi.decode_one(list(sent))
                assert len(sent) == len(tags) == len(tags_pred)
                feat_gold = feat_vect(sent, tags)
                feat_pred = feat_vect(sent, tags_pred)
                for feat in feat_pred:
                    self.v[feat] -= feat_pred[feat]
                for feat in feat_gold:
                    self.v[feat] += feat_gold[feat]


if __name__ == "__main__":
    train_file = 'gene.train'
    outpath = sys.argv[1]
    model = Perceptron(train_file)
    model.train(outpath)
