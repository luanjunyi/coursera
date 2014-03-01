from collections import defaultdict

def feat_score(i, t, u, v, sent, vec):
    ret = 0.0
    token = sent[i]
    for l in [1, 2, 3]:
        if len(token) >= l:
            suffix = token[-l:]
            prefix = token[:l].lower()
            ret += vec["__SUFFIX__", suffix, v]
            ret += vec["__PREFIX__", prefix, v]
    if i >= 2:
        ret += vec["__PREVWORD__", sent[i-1], v]
    return ret + vec['TRIGRAM', t, u, v] + vec['TAG', token, v];

def tag(tags, idx):
    if idx < 0:
        return '__*__'
    if idx >= len(tags):
        return 'STOP'
    return tags[idx]


def feat_vect(sent, tags):
    n = len(sent)
    ret = defaultdict(int)
    for i in xrange(n+1):
        u, v, t = tag(tags, i-2), tag(tags, i-1), tag(tags, i)
        ret['TRIGRAM', u, v, t] += 1
        if i < n:
            w = sent[i]
            ret['TAG', w, t] += 1
            for l in [1, 2, 3]:
                if len(w) >= l:
                    # suffix features
                    suffix = w[-l:]
                    ret['__SUFFIX__', suffix, t] += 1
                    # prefix features
                    prefix = w[:l].lower()
                    ret['__PREFIX__', prefix, t] += 1

            # previous word
            if i > 0:
                ret['__PREVWORD__', sent[i-1], t] += 1
            else:
                ret['__PREVWORD__', "__*__", t] += 1
    return ret

