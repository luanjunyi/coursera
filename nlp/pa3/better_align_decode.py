import sys
from collections import defaultdict
from ibm2_decode import IBM2Decode
from ibm2_train import IBM2

def argmax(ls):
    if not ls:
        return None, 0.0
    return max(ls, key = lambda x: x[1])

def get_mat_val(mat, i, j):
    return 1 if 0 <= i < len(mat) and 0 <= j < len(mat[i]) and mat[i][j] > 0 else 0

def adj_count(mat, i, j):
    return sum([get_mat_val(mat, i+di, j+dj) 
                for di in range(-1, 2, 1) for dj in xrange(-1, 2, 1)])

if __name__ == "__main__":
    from_file = sys.argv[1] # Spanish corpus
    to_file = sys.argv[2] # English corpus

    en2es = IBM2Decode(open("en2es.ibm2.model", "r"))
    en2es.load_file(to_file, from_file)
    es2en = IBM2Decode(open("ibm2.model", "r"))
    es2en.load_file(from_file, to_file)
    size = en2es.size()
    for k in xrange(size):
        row = es2en.get_alignment(k)
        col = en2es.get_alignment(k)
        m = len(es2en.to_corpus[k])
        n = len(es2en.from_corpus[k]) + 1
        mat = list()
        e_left = set(range(m))
        f_left = set(range(n))
        e_match = defaultdict(set)
        f_match = defaultdict(set)

        for i in xrange(m):
            mat.append([0] * n)

        for i, c in enumerate(row):
            mat[c][i+1] += 1
            e_match[c].add(i+1)
            f_match[i+1].add(c)
        for i, r in enumerate(col):
            mat[i+1][r] += 1
            e_match[i+1].add(r)
            f_match[r].add(i+1)
            if mat[i+1][r] == 2:
                e_left.remove(i+1)
                f_left.remove(r)
                print "%d %d %d" % (k + 1, i + 1, r)
        
        # processed = set()
        # for ei in e_left:
        #     if ei == 0:
        #         processed.add(ei)
        #         continue
        #     j, score = argmax([(j, adj_count(mat, ei, j)) for j in e_match[ei]])
        #     if score > 0.0:
        #         mat[ei][j] = 2
        #         processed.add(ei)
        #         if j != 0:
        #             print "%d %d %d" % (k + 1, ei, j)
        # e_left -= processed
        
        # processed = set()
        # for fi in f_left:
        #     if fi == 0:
        #         processed.add(fi)
        #         continue
        #     j, score = argmax([(j, adj_count(mat, j, fi)) for j in f_match[fi]])
        #     if score > 0.0:
        #         mat[j][fi] = 2
        #         processed.add(fi)
        #         if j != 0:
        #             print "%d %d %d" % (k + 1, j, fi)
        # f_left -= processed

